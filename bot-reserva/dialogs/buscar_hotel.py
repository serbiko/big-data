from botbuilder.core import MessageFactory, UserState
from botbuilder.dialogs import ComponentDialog, WaterfallDialog, WaterfallStepContext
from botbuilder.dialogs.prompts import TextPrompt, PromptOptions

class BuscarHotelDialog(ComponentDialog):
    def __init__(self, user_state: UserState):
        super(BuscarHotelDialog, self).__init__("BuscarHotelDialog")
        self.user_state = user_state
        
        self.add_dialog(TextPrompt("cidadePrompt"))
        self.add_dialog(TextPrompt("checkinPrompt"))
        self.add_dialog(TextPrompt("checkoutPrompt"))
        self.add_dialog(TextPrompt("pessoasPrompt"))
        
        self.add_dialog(
            WaterfallDialog(
                "BuscarHotelDialog",
                [
                    self.prompt_cidade_step,
                    self.prompt_checkin_step,
                    self.prompt_checkout_step,
                    self.prompt_pessoas_step,
                    self.process_hotel_step
                ]
            )
        )
                
        self.initial_dialog_id = "BuscarHotelDialog"
        
    async def prompt_cidade_step(self, step_context: WaterfallStepContext):
        return await step_context.prompt(
            "cidadePrompt",
            PromptOptions(prompt=MessageFactory.text("Digite a cidade onde deseja reservar o hotel:"))
        )

    async def prompt_checkin_step(self, step_context: WaterfallStepContext):
        step_context.values["cidade"] = step_context.result
        return await step_context.prompt(
            "checkinPrompt",
            PromptOptions(prompt=MessageFactory.text("Digite a data de check-in (DD/MM/AAAA):"))
        )

    async def prompt_checkout_step(self, step_context: WaterfallStepContext):
        step_context.values["checkin"] = step_context.result
        return await step_context.prompt(
            "checkoutPrompt",
            PromptOptions(prompt=MessageFactory.text("Digite a data de check-out (DD/MM/AAAA):"))
        )

    async def prompt_pessoas_step(self, step_context: WaterfallStepContext):
        step_context.values["checkout"] = step_context.result
        return await step_context.prompt(
            "pessoasPrompt",
            PromptOptions(prompt=MessageFactory.text("Digite o número de pessoas na reserva:"))
        )

    async def process_hotel_step(self, step_context: WaterfallStepContext):
        cidade = step_context.values["cidade"]
        checkin = step_context.values["checkin"]
        checkout = step_context.values["checkout"]
        pessoas = step_context.result

        # TODO: Chamada à API de hotéis
        resposta = f"Buscando hotéis em {cidade} de {checkin} até {checkout} para {pessoas} pessoa(s)...\nEncontrei 5 opções disponíveis."
        
        await step_context.context.send_activity(MessageFactory.text(resposta))
        return await step_context.end_dialog()
