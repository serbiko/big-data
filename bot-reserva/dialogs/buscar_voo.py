from botbuilder.core import MessageFactory, UserState
from botbuilder.dialogs import ComponentDialog, WaterfallDialog, WaterfallStepContext
from botbuilder.dialogs.prompts import TextPrompt, PromptOptions, ChoicePrompt
from botbuilder.dialogs.choices import Choice, ListStyle
from dataclasses import dataclass
import random
import string
from datetime import datetime

from db import criar_reserva  # cria reserva no Postgres


@dataclass
class Voo:
    cia: str
    saida: str
    chegada: str
    preco: float


class BuscarVooDialog(ComponentDialog):
    def __init__(self, user_state: UserState):
        super(BuscarVooDialog, self).__init__("BuscarVooDialog")
        self.user_state = user_state

        self.add_dialog(TextPrompt("origemPrompt"))
        self.add_dialog(TextPrompt("destinoPrompt"))
        self.add_dialog(TextPrompt("dataPrompt"))
        self.add_dialog(ChoicePrompt("vooOptionsPrompt"))

        self.add_dialog(
            WaterfallDialog(
                "BuscarVooDialog",
                [
                    self.prompt_origem_step,
                    self.prompt_destino_step,
                    self.prompt_data_step,
                    self.mostrar_opcoes_step,
                    self.selecionar_opcao_step,
                ],
            )
        )

        self.initial_dialog_id = "BuscarVooDialog"

    async def prompt_origem_step(self, step_context: WaterfallStepContext):
        return await step_context.prompt(
            "origemPrompt",
            PromptOptions(prompt=MessageFactory.text("Digite a cidade de origem do voo:")),
        )

    async def prompt_destino_step(self, step_context: WaterfallStepContext):
        step_context.values["origem"] = step_context.result
        return await step_context.prompt(
            "destinoPrompt",
            PromptOptions(prompt=MessageFactory.text("Digite a cidade de destino do voo:")),
        )

    async def prompt_data_step(self, step_context: WaterfallStepContext):
        step_context.values["destino"] = step_context.result
        return await step_context.prompt(
            "dataPrompt",
            PromptOptions(prompt=MessageFactory.text("Digite a data do voo (DD/MM/AAAA):")),
        )

    async def mostrar_opcoes_step(self, step_context: WaterfallStepContext):
        step_context.values["data"] = step_context.result
        origem = step_context.values["origem"]
        destino = step_context.values["destino"]
        data = step_context.values["data"]

        opcoes = [
            Voo("Azul",  "07:10", "08:20", 350.00),
            Voo("LATAM", "10:35", "11:45", 429.90),
            Voo("GOL",   "18:20", "19:30", 399.00),
        ]
        step_context.values["opcoes_voo"] = opcoes

        await step_context.context.send_activity(
            MessageFactory.text(
                f"Buscando voos de {origem} para {destino} em {data}...\n"
                f"Encontrei {len(opcoes)} opções:"
            )
        )

        rotulos = [
            f"1) {opcoes[0].cia} {opcoes[0].saida}-{opcoes[0].chegada} | R$ {opcoes[0].preco:.2f}",
            f"2) {opcoes[1].cia} {opcoes[1].saida}-{opcoes[1].chegada} | R$ {opcoes[1].preco:.2f}",
            f"3) {opcoes[2].cia} {opcoes[2].saida}-{opcoes[2].chegada} | R$ {opcoes[2].preco:.2f}",
        ]
        choices = [Choice(r) for r in rotulos]

        return await step_context.prompt(
            "vooOptionsPrompt",
            PromptOptions(
                prompt=MessageFactory.text("Escolha uma opção de voo:"),
                choices=choices,
                style=ListStyle.suggested_action,  # compatível
            ),
        )

    async def selecionar_opcao_step(self, step_context: WaterfallStepContext):
        result = step_context.result
        escolha_label = getattr(result, "value", None) or str(result)

        opcoes = step_context.values["opcoes_voo"]
        idx = 0
        if escolha_label.startswith("2)"):
            idx = 1
        elif escolha_label.startswith("3)"):
            idx = 2
        escolhido: Voo = opcoes[idx]

        # gera código e cria a reserva no Postgres
        codigo = "V-" + "".join(random.choices(string.ascii_uppercase + string.digits, k=5))
        origem = step_context.values["origem"]
        destino = step_context.values["destino"]
        data = step_context.values["data"]

        try:
            dia = datetime.strptime(data, "%d/%m/%Y").strftime("%Y-%m-%d")
            data_hora = f"{dia} {escolhido.saida}:00"
        except Exception:
            data_hora = None  # deixa NULL se não conseguir

        try:
            criar_reserva(
                reserva_id=codigo,
                passageiro="Cliente",
                origem=origem,
                destino=destino,
                data_hora=data_hora,
                localizador="".join(random.choices(string.ascii_uppercase + string.digits, k=5)),
                valor=float(escolhido.preco),
                status="Confirmada",
            )
        except Exception:
            # não derrube o diálogo se o DB falhar
            pass

        confirmacao = (
            f"✅ Voo selecionado:\n"
            f"- {escolhido.cia} {escolhido.saida}-{escolhido.chegada}\n"
            f"- R$ {escolhido.preco:.2f}\n"
            f"- {origem} → {destino} em {data}\n"
            f"🧾 **Código da reserva**: {codigo}\n\n"
            f"Agora você pode usar esse código em **Consultar Reserva / Status / Cancelar**."
        )
        await step_context.context.send_activity(MessageFactory.text(confirmacao))
        return await step_context.end_dialog()
