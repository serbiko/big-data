from botbuilder.core import MessageFactory, UserState
from botbuilder.dialogs import ComponentDialog, WaterfallDialog, WaterfallStepContext
from botbuilder.dialogs.prompts import TextPrompt, PromptOptions

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
                    self.process_reserva_step
                ]
            )
        )
                
        self.initial_dialog_id = "ConsultarReservaDialog"
        
    async def prompt_reserva_step(self, step_context: WaterfallStepContext):
        return await step_context.prompt(
            "reservaPrompt",
            PromptOptions(prompt=MessageFactory.text("Digite o número da reserva que deseja consultar:"))
        )

    async def process_reserva_step(self, step_context: WaterfallStepContext):
        reserva_id = step_context.result

        # TODO: Consulta no banco de dados
        resposta = f"Consulta da reserva {reserva_id}: Voo São Paulo → Rio em 10/10/2025 às 20h. Status: Confirmada."
        
        await step_context.context.send_activity(MessageFactory.text(resposta))
        return await step_context.end_dialog()
