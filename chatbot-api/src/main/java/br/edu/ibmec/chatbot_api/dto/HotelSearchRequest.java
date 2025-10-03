package br.edu.ibmec.chatbot_api.dto;

public class HotelSearchRequest {
    private String cidade;
    private String checkin;
    private String checkout;
    private int pessoas;

    public HotelSearchRequest() {}

    public HotelSearchRequest(String cidade, String checkin, String checkout, int pessoas) {
        this.cidade = cidade;
        this.checkin = checkin;
        this.checkout = checkout;
        this.pessoas = pessoas;
    }

    public String getCidade() { return cidade; }
    public void setCidade(String cidade) { this.cidade = cidade; }

    public String getCheckin() { return checkin; }
    public void setCheckin(String checkin) { this.checkin = checkin; }

    public String getCheckout() { return checkout; }
    public void setCheckout(String checkout) { this.checkout = checkout; }

    public int getPessoas() { return pessoas; }
    public void setPessoas(int pessoas) { this.pessoas = pessoas; }
}
