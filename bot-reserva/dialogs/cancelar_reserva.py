from botbuilder.core import MessageFactory, UserState
from botbuilder.dialogs import ComponentDialog, WaterfallDialog, WaterfallStepContext
from botbuilder.dialogs.prompts import TextPrompt, PromptOptions

class CancelarReservaDialog(ComponentDialog):
    def __init__(self, user_state: UserState):
        super(CancelarReservaDialog, self).__init__("CancelarReservaDialog")
        self.user_state = user_state
        
        self.add_dialog(TextPrompt("reservaPrompt"))
        
        self.add_dialog(
            WaterfallDialog(
                "CancelarReservaDialog",
                [
                    self.prompt_reserva_step,
                    self.process_cancelar_step
                ]
            )
        )
                
        self.initial_dialog_id = "CancelarReservaDialog"
        
    async def prompt_reserva_step(self, step_context: WaterfallStepContext):
        return await step_context.prompt(
            "reservaPrompt",
            PromptOptions(prompt=MessageFactory.text("Digite o número da reserva que deseja cancelar:"))
        )

    async def process_cancelar_step(self, step_context: WaterfallStepContext):
        reserva_id = step_context.result

        # TODO: lógica de cancelamento no banco ou API
        resposta = f"A reserva {reserva_id} foi cancelada com sucesso."
        
        await step_context.context.send_activity(MessageFactory.text(resposta))
        return await step_context.end_dialog()
