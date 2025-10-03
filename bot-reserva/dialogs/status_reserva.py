from botbuilder.core import MessageFactory, UserState
from botbuilder.dialogs import ComponentDialog, WaterfallDialog, WaterfallStepContext
from botbuilder.dialogs.prompts import TextPrompt, PromptOptions

class StatusReservaDialog(ComponentDialog):
    def __init__(self, user_state: UserState):
        super(StatusReservaDialog, self).__init__("StatusReservaDialog")
        self.user_state = user_state
        
        self.add_dialog(TextPrompt("reservaPrompt"))
        
        self.add_dialog(
            WaterfallDialog(
                "StatusReservaDialog",
                [
                    self.prompt_reserva_step,
                    self.process_status_step
                ]
            )
        )
                
        self.initial_dialog_id = "StatusReservaDialog"
        
    async def prompt_reserva_step(self, step_context: WaterfallStepContext):
        return await step_context.prompt(
            "reservaPrompt",
            PromptOptions(prompt=MessageFactory.text("Digite o número da reserva que deseja consultar o status:"))
        )

    async def process_status_step(self, step_context: WaterfallStepContext):
        reserva_id = step_context.result

        # TODO: lógica de consulta real no banco ou API
        resposta = f"O status da reserva {reserva_id} é: Confirmada ✅."
        
        await step_context.context.send_activity(MessageFactory.text(resposta))
        return await step_context.end_dialog()
