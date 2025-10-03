from botbuilder.core import MessageFactory, UserState
from botbuilder.dialogs import ComponentDialog, WaterfallDialog, WaterfallStepContext
from botbuilder.dialogs.prompts import TextPrompt, PromptOptions

class BuscarVooDialog(ComponentDialog):
    def __init__(self, user_state: UserState):
        super(BuscarVooDialog, self).__init__("BuscarVooDialog")
        self.user_state = user_state
        
        self.add_dialog(TextPrompt("origemPrompt"))
        self.add_dialog(TextPrompt("destinoPrompt"))
        self.add_dialog(TextPrompt("dataPrompt"))
        
        self.add_dialog(
            WaterfallDialog(
                "BuscarVooDialog",
                [
                    self.prompt_origem_step,
                    self.prompt_destino_step,
                    self.prompt_data_step,
                    self.process_voo_step
                ]
            )
        )
                
        self.initial_dialog_id = "BuscarVooDialog"
        
    async def prompt_origem_step(self, step_context: WaterfallStepContext):
        return await step_context.prompt(
            "origemPrompt",
            PromptOptions(prompt=MessageFactory.text("Digite a cidade de origem do voo:"))
        )

    async def prompt_destino_step(self, step_context: WaterfallStepContext):
        step_context.values["origem"] = step_context.result
        return await step_context.prompt(
            "destinoPrompt",
            PromptOptions(prompt=MessageFactory.text("Digite a cidade de destino do voo:"))
        )

    async def prompt_data_step(self, step_context: WaterfallStepContext):
        step_context.values["destino"] = step_context.result
        return await step_context.prompt(
            "dataPrompt",
            PromptOptions(prompt=MessageFactory.text("Digite a data do voo (DD/MM/AAAA):"))
        )

    async def process_voo_step(self, step_context: WaterfallStepContext):
        origem = step_context.values["origem"]
        destino = step_context.values["destino"]
        data = step_context.result

        # TODO: Chamada à API de voos
        resposta = f"Buscando voos de {origem} para {destino} em {data}...\nEncontrei 3 opções disponíveis."
        
        await step_context.context.send_activity(MessageFactory.text(resposta))
        return await step_context.end_dialog()
