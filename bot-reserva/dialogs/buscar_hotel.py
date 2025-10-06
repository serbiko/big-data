from botbuilder.core import MessageFactory, UserState
from botbuilder.dialogs import ComponentDialog, WaterfallDialog, WaterfallStepContext
from botbuilder.dialogs.prompts import TextPrompt, PromptOptions, ChoicePrompt
from botbuilder.dialogs.choices import Choice, ListStyle
from dataclasses import dataclass
import random
import string
from datetime import datetime

from db import criar_reserva  # << NOVO


@dataclass
class Hotel:
    nome: str
    estrelas: int
    preco_noite: float
    bairro: str


class BuscarHotelDialog(ComponentDialog):
    def __init__(self, user_state: UserState):
        super(BuscarHotelDialog, self).__init__("BuscarHotelDialog")
        self.user_state = user_state

        self.add_dialog(TextPrompt("cidadePrompt"))
        self.add_dialog(TextPrompt("checkinPrompt"))
        self.add_dialog(TextPrompt("checkoutPrompt"))
        self.add_dialog(TextPrompt("pessoasPrompt"))
        self.add_dialog(ChoicePrompt("hotelOptionsPrompt"))

        self.add_dialog(
            WaterfallDialog(
                "BuscarHotelDialog",
                [
                    self.prompt_cidade_step,
                    self.prompt_checkin_step,
                    self.prompt_checkout_step,
                    self.prompt_pessoas_step,
                    self.mostrar_opcoes_step,
                    self.selecionar_opcao_step,
                ]
            )
        )

        self.initial_dialog_id = "BuscarHotelDialog"

    async def prompt_cidade_step(self, step_context: WaterfallStepContext):
        return await step_context.prompt(
            "cidadePrompt",
            PromptOptions(prompt=MessageFactory.text("Digite a cidade onde deseja reservar o hotel:")),
        )

    async def prompt_checkin_step(self, step_context: WaterfallStepContext):
        step_context.values["cidade"] = step_context.result
        return await step_context.prompt(
            "checkinPrompt",
            PromptOptions(prompt=MessageFactory.text("Digite a data de check-in (DD/MM/AAAA):")),
        )

    async def prompt_checkout_step(self, step_context: WaterfallStepContext):
        step_context.values["checkin"] = step_context.result
        return await step_context.prompt(
            "checkoutPrompt",
            PromptOptions(prompt=MessageFactory.text("Digite a data de check-out (DD/MM/AAAA):")),
        )

    async def prompt_pessoas_step(self, step_context: WaterfallStepContext):
        step_context.values["checkout"] = step_context.result
        return await step_context.prompt(
            "pessoasPrompt",
            PromptOptions(prompt=MessageFactory.text("Digite o número de pessoas na reserva:")),
        )

    async def mostrar_opcoes_step(self, step_context: WaterfallStepContext):
        step_context.values["pessoas"] = step_context.result

        cidade = step_context.values["cidade"]
        checkin = step_context.values["checkin"]
        checkout = step_context.values["checkout"]
        pessoas = step_context.values["pessoas"]

        opcoes = [
            Hotel("Hotel Atlântico", 4, 420.00, "Copacabana"),
            Hotel("Ipanema Vista",   5, 690.00, "Ipanema"),
            Hotel("Centro Confort",  3, 289.90, "Centro"),
        ]
        step_context.values["opcoes_hotel"] = opcoes

        await step_context.context.send_activity(
            MessageFactory.text(
                f"Buscando hotéis em {cidade} de {checkin} até {checkout} para {pessoas} pessoa(s)...\n"
                f"Encontrei {len(opcoes)} opções:"
            )
        )

        rotulos = [
            f"1) {opcoes[0].nome} • {opcoes[0].estrelas}★ • R$ {opcoes[0].preco_noite:.2f}/noite • {opcoes[0].bairro}",
            f"2) {opcoes[1].nome} • {opcoes[1].estrelas}★ • R$ {opcoes[1].preco_noite:.2f}/noite • {opcoes[1].bairro}",
            f"3) {opcoes[2].nome} • {opcoes[2].estrelas}★ • R$ {opcoes[2].preco_noite:.2f}/noite • {opcoes[2].bairro}",
        ]
        choices = [Choice(r) for r in rotulos]

        return await step_context.prompt(
            "hotelOptionsPrompt",
            PromptOptions(
                prompt=MessageFactory.text("Escolha uma opção de hotel:"),
                choices=choices,
                style=ListStyle.suggested_action,
            ),
        )

    async def selecionar_opcao_step(self, step_context: WaterfallStepContext):
        result = step_context.result
        escolha_label = getattr(result, "value", None) or str(result)

        opcoes = step_context.values["opcoes_hotel"]
        idx = 0
        if escolha_label.startswith("2)"):
            idx = 1
        elif escolha_label.startswith("3)"):
            idx = 2
        escolhido: Hotel = opcoes[idx]

        # gera código e cria a reserva no Postgres
        codigo = "H-" + "".join(random.choices(string.ascii_uppercase + string.digits, k=5))
        cidade = step_context.values["cidade"]
        checkin = step_context.values["checkin"]
        checkout = step_context.values["checkout"]
        pessoas = step_context.values["pessoas"]

        # para hotel, salvamos sem data_hora precisa; podemos usar check-in como data base
        try:
            dia_checkin = datetime.strptime(checkin, "%d/%m/%Y").strftime("%Y-%m-%d")
            data_hora = f"{dia_checkin} 15:00:00"  # check-in 15:00 (mock)
        except Exception:
            data_hora = None

        try:
            criar_reserva(
                reserva_id=codigo,
                passageiro="Cliente",
                origem=cidade,
                destino=f"{escolhido.nome} ({escolhido.bairro})",
                data_hora=data_hora,
                localizador="".join(random.choices(string.ascii_uppercase + string.digits, k=5)),
                valor=float(escolhido.preco_noite),
                status="Confirmada",
            )
        except Exception:
            pass

        confirmacao = (
            "✅ Hotel selecionado:\n"
            f"- {escolhido.nome} ({escolhido.estrelas}★) — {escolhido.bairro}\n"
            f"- R$ {escolhido.preco_noite:.2f}/noite\n"
            f"- {cidade} • {checkin} → {checkout} • {pessoas} pessoa(s)\n"
            f"🧾 **Código da reserva**: {codigo}\n\n"
            "Agora você pode usar esse código em **Consultar Reserva / Status / Cancelar**."
        )
        await step_context.context.send_activity(MessageFactory.text(confirmacao))
        return await step_context.end_dialog()
