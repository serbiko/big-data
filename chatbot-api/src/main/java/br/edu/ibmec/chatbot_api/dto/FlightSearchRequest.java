package br.edu.ibmec.chatbot_api.dto;

public class FlightSearchRequest {
    private String origem;
    private String destino;
    private String data;

    public FlightSearchRequest() {}

    public FlightSearchRequest(String origem, String destino, String data) {
        this.origem = origem;
        this.destino = destino;
        this.data = data;
    }

    public String getOrigem() { return origem; }
    public void setOrigem(String origem) { this.origem = origem; }

    public String getDestino() { return destino; }
    public void setDestino(String destino) { this.destino = destino; }

    public String getData() { return data; }
    public void setData(String data) { this.data = data; }
}
