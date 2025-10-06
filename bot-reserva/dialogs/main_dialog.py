from botbuilder.core import MessageFactory, UserState
from botbuilder.dialogs import ComponentDialog, WaterfallDialog, WaterfallStepContext
from botbuilder.dialogs.prompts import ChoicePrompt, PromptOptions
from botbuilder.dialogs.choices import Choice, ListStyle
from dialogs.buscar_voo import BuscarVooDialog
from dialogs.buscar_hotel import BuscarHotelDialog
from dialogs.consultar_reserva import ConsultarReservaDialog
from dialogs.cancelar_reserva import CancelarReservaDialog
from dialogs.status_reserva import StatusReservaDialog


class MainDialog(ComponentDialog):
    def __init__(self, user_state: UserState):
        super(MainDialog, self).__init__("MainDialog")

        self.user_state = user_state
        self.add_dialog(ChoicePrompt(ChoicePrompt.__name__))

        self.add_dialog(BuscarVooDialog(self.user_state))
        self.add_dialog(BuscarHotelDialog(self.user_state))
        self.add_dialog(ConsultarReservaDialog(self.user_state))
        self.add_dialog(CancelarReservaDialog(self.user_state))
        self.add_dialog(StatusReservaDialog(self.user_state))

        self.add_dialog(
            WaterfallDialog(
                "MainDialog",
                [
                    self.prompt_option_step,
                    self.process_option_step,
                    self.loop_menu_step,
                ],
            )
        )

        self.initial_dialog_id = "MainDialog"

    async def prompt_option_step(self, step_context: WaterfallStepContext):
        return await step_context.prompt(
            ChoicePrompt.__name__,
            PromptOptions(
                prompt=MessageFactory.text("Escolha a opção desejada:"),
                choices=[
                    Choice("Buscar Voo"),
                    Choice("Buscar Hotel"),
                    Choice("Consultar Reserva"),
                    Choice("Cancelar Reserva"),
                    Choice("Status da Reserva"),
                ],
                style=ListStyle.suggested_action,
            ),
        )

    async def process_option_step(self, step_context: WaterfallStepContext):
        option = step_context.result.value

        if option == "Buscar Voo":
            return await step_context.begin_dialog("BuscarVooDialog")
        elif option == "Buscar Hotel":
            return await step_context.begin_dialog("BuscarHotelDialog")
        elif option == "Consultar Reserva":
            return await step_context.begin_dialog("ConsultarReservaDialog")
        elif option == "Cancelar Reserva":
            return await step_context.begin_dialog("CancelarReservaDialog")
        elif option == "Status da Reserva":
            return await step_context.begin_dialog("StatusReservaDialog")

        # fallback: volta ao menu
        return await step_context.replace_dialog("MainDialog")

    async def loop_menu_step(self, step_context: WaterfallStepContext):
        return await step_context.replace_dialog("MainDialog")
