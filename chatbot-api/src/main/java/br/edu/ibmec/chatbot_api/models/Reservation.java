package br.edu.ibmec.chatbot_api.models;

public class Reservation {
    private String id;
    private ReservationType tipo;
    private ReservationStatus status;
    private String descricao;

    public Reservation() {}

    public Reservation(String id, ReservationType tipo, ReservationStatus status, String descricao) {
        this.id = id;
        this.tipo = tipo;
        this.status = status;
        this.descricao = descricao;
    }

    public String getId() { return id; }
    public void setId(String id) { this.id = id; }

    public ReservationType getTipo() { return tipo; }
    public void setTipo(ReservationType tipo) { this.tipo = tipo; }

    public ReservationStatus getStatus() { return status; }
    public void setStatus(ReservationStatus status) { this.status = status; }

    public String getDescricao() { return descricao; }
    public void setDescricao(String descricao) { this.descricao = descricao; }
}
