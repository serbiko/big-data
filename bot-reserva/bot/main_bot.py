# main_bot.py
from botbuilder.core import ActivityHandler, TurnContext, MessageFactory, UserState, ConversationState
from botbuilder.schema import ChannelAccount, ActivityTypes
from botbuilder.dialogs import Dialog
from helpers.DialogHelper import DialogHelper

# << novo: função que grava no Postgres >>
from db import salvar_conversa


class MainBot(ActivityHandler):
    def __init__(
        self,
        dialog: Dialog,
        conversation_state: ConversationState,
        user_state: UserState,
    ):
        self.dialog = dialog
        self.conversation_state = conversation_state
        self.user_state = user_state

    async def on_turn(self, turn_context: TurnContext):
        # executa o fluxo padrão (chama on_message_activity / on_members_added etc.)
        await super().on_turn(turn_context)

        # salva mudanças de estado ao final do turno
        await self.conversation_state.save_changes(turn_context)
        await self.user_state.save_changes(turn_context)

    async def on_message_activity(self, turn_context: TurnContext):
        # 1) ENTRADA: usuário -> bot
        act = turn_context.activity
        if act.type == ActivityTypes.message:
            usuario = (
                (act.from_property.name or act.from_property.id)
                if act.from_property
                else "usuario"
            )
            texto = act.text or ""
            salvar_conversa(usuario, texto)

        # 2) Interceptar SAÍDA: bot -> usuário (qualquer send dos diálogos neste turno)
        original_send = turn_context.send_activities  # método já "bound"

        async def patched_send(activities):
            result = await original_send(activities)
            # registra todas as mensagens de texto enviadas pelo bot
            for a in activities:
                if a.type == ActivityTypes.message and getattr(a, "text", None):
                    salvar_conversa("bot", a.text)
            return result

        # monkey-patch apenas para este turno
        turn_context.send_activities = patched_send

        # 3) segue o fluxo normal do seu diálogo principal
        await DialogHelper.run_dialog(
            self.dialog,
            turn_context,
            self.conversation_state.create_property("MainDialogState"),
        )

    async def on_members_added_activity(
        self, members_added: ChannelAccount, turn_context: TurnContext
    ):
        for member_added in members_added:
            if member_added.id != turn_context.activity.recipient.id:
                await turn_context.send_activity(
                    MessageFactory.text(
                        "Seja bem-vindo(a) ao bot de atendimento do André e do Raí. "
                        "Digite uma mensagem para iniciar o atendimento."
                    )
                )
