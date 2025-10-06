from botbuilder.core import MessageFactory, UserState
from botbuilder.dialogs import ComponentDialog, WaterfallDialog, WaterfallStepContext
from botbuilder.dialogs.prompts import TextPrompt, PromptOptions, ChoicePrompt
from botbuilder.dialogs.choices import Choice, ListStyle
from db import get_reserva, cancelar_reserva


class CancelarReservaDialog(ComponentDialog):
    def __init__(self, user_state: UserState):
        super(CancelarReservaDialog, self).__init__("CancelarReservaDialog")
        self.user_state = user_state

        self.add_dialog(TextPrompt("reservaPrompt"))
        self.add_dialog(ChoicePrompt("confirmPrompt"))

        self.add_dialog(
            WaterfallDialog(
                "CancelarReservaDialog",
                [
                    self.prompt_reserva_step,     # pede o número
                    self.resumo_e_confirma_step,  # mostra detalhes + confirma
                    self.process_cancelar_step,   # executa cancelamento
                ],
            )
        )

        self.initial_dialog_id = "CancelarReservaDialog"

    async def prompt_reserva_step(self, step_context: WaterfallStepContext):
        return await step_context.prompt(
            "reservaPrompt",
            PromptOptions(
                prompt=MessageFactory.text("Digite o número da reserva que deseja cancelar:")
            ),
        )

    async def resumo_e_confirma_step(self, step_context: WaterfallStepContext):
        reserva_id = (step_context.result or "").strip()
        step_context.values["reserva_id"] = reserva_id

        res = get_reserva(reserva_id)
        if not res:
            await step_context.context.send_activity(
                MessageFactory.text(f"❌ Reserva **{reserva_id}** não encontrada.")
            )
            return await step_context.end_dialog()

        # formata campos
        data_hora = res["data_hora"]
        data_fmt = data_hora.strftime("%d/%m/%Y às %H:%M") if hasattr(data_hora, "strftime") else str(data_hora)
        valor_fmt = f"R$ {float(res['valor']):.2f}" if res.get("valor") is not None else "-"

        resumo = (
            f"📄 Detalhes da reserva {res['id']}:\n"
            f"- Passageiro: {res.get('passageiro','-')}\n"
            f"- Trecho: {res.get('origem','-')} → {res.get('destino','-')}\n"
            f"- Data/Hora: {data_fmt}\n"
            f"- Localizador: {res.get('localizador','-')}\n"
            f"- Valor: {valor_fmt}\n"
            f"- Status: {res.get('status','-')}"
        )
        await step_context.context.send_activity(MessageFactory.text(resumo))

        # opções sem ChoiceFactory
        return await step_context.prompt(
            "confirmPrompt",
            PromptOptions(
                prompt=MessageFactory.text("Tem certeza que deseja cancelar esta reserva?"),
                choices=[Choice("Sim"), Choice("Não")],
                style=ListStyle.suggested_action,  # mais estável que hero_card
            ),
        )

    async def process_cancelar_step(self, step_context: WaterfallStepContext):
        # pode vir FoundChoice (com .value) ou string simples
        result = step_context.result
        escolha = getattr(result, "value", None) or str(result)
        reserva_id = step_context.values["reserva_id"]

        if escolha.lower().startswith("n"):  # "Não"
            await step_context.context.send_activity(
                MessageFactory.text("❎ Cancelamento abortado. A reserva permanece ativa.")
            )
            await step_context.context.send_activity(
                MessageFactory.text("Você pode digitar **menu** para escolher outra ação.")
            )
            return await step_context.end_dialog()

        # "Sim": tenta cancelar de verdade
        ok = cancelar_reserva(reserva_id)
        if not ok:
            await step_context.context.send_activity(
                MessageFactory.text(
                    "⚠️ Não foi possível cancelar. Ela pode já estar **Cancelada** ou não existir."
                )
            )
            return await step_context.end_dialog()

        await step_context.context.send_activity(
            MessageFactory.text(f"✅ A reserva **{reserva_id}** foi **cancelada**.")
        )
        await step_context.context.send_activity(
            MessageFactory.text("Você pode digitar **menu** para escolher outra ação.")
        )
        return await step_context.end_dialog()
