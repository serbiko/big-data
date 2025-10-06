from botbuilder.core import MessageFactory, UserState
from botbuilder.dialogs import ComponentDialog, WaterfallDialog, WaterfallStepContext
from botbuilder.dialogs.prompts import TextPrompt, PromptOptions
from db import get_reserva


class ConsultarReservaDialog(ComponentDialog):
    def __init__(self, user_state: UserState):
        super(ConsultarReservaDialog, self).__init__("ConsultarReservaDialog")
        self.user_state = user_state

        self.add_dialog(TextPrompt("reservaPrompt"))

        self.add_dialog(
            WaterfallDialog(
                "ConsultarReservaDialog",
                [
                    self.prompt_reserva_step,
                    self.process_reserva_step,
                ],
            )
        )

        self.initial_dialog_id = "ConsultarReservaDialog"

    async def prompt_reserva_step(self, step_context: WaterfallStepContext):
        return await step_context.prompt(
            "reservaPrompt",
            PromptOptions(
                prompt=MessageFactory.text("Digite o número da reserva que deseja consultar:")
            ),
        )

    async def process_reserva_step(self, step_context: WaterfallStepContext):
        reserva_id = (step_context.result or "").strip()
        res = get_reserva(reserva_id)

        if not res:
            await step_context.context.send_activity(
                MessageFactory.text(f"❌ Reserva **{reserva_id}** não encontrada.")
            )
            await step_context.context.send_activity(
                MessageFactory.text("Você pode digitar **menu** para escolher outra ação.")
            )
            return await step_context.end_dialog()

        # formata data/hora do Postgres (timestamp) se vier como datetime
        data_hora = res["data_hora"]
        data_fmt = data_hora.strftime("%d/%m/%Y às %H:%M") if hasattr(data_hora, "strftime") else str(data_hora)
        valor_fmt = f"R$ {float(res['valor']):.2f}" if res.get("valor") is not None else "-"

        detalhes = (
            f"📄 Consulta da reserva {res['id']}:\n"
            f"- Passageiro: {res.get('passageiro','-')}\n"
            f"- Voo: {res.get('origem','-')} → {res.get('destino','-')}\n"
            f"- Data/Hora: {data_fmt}\n"
            f"- Localizador: {res.get('localizador','-')}\n"
            f"- Valor: {valor_fmt}\n"
            f"- Status: {res.get('status','-')}"
        )
        await step_context.context.send_activity(MessageFactory.text(detalhes))
        await step_context.context.send_activity(
            MessageFactory.text("Você pode digitar **menu** para escolher outra ação.")
        )
        return await step_context.end_dialog()
