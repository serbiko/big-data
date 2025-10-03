package br.edu.ibmec.chatbot_api.dto;

public class HotelOption {
    private String nome;
    private String cidade;
    private String checkin;
    private String checkout;
    private int estrelas;
    private double precoNoite;

    public HotelOption() {}

    public HotelOption(String nome, String cidade, String checkin, String checkout, int estrelas, double precoNoite) {
        this.nome = nome;
        this.cidade = cidade;
        this.checkin = checkin;
        this.checkout = checkout;
        this.estrelas = estrelas;
        this.precoNoite = precoNoite;
    }

    public String getNome() { return nome; }
    public void setNome(String nome) { this.nome = nome; }

    public String getCidade() { return cidade; }
    public void setCidade(String cidade) { this.cidade = cidade; }

    public String getCheckin() { return checkin; }
    public void setCheckin(String checkin) { this.checkin = checkin; }

    public String getCheckout() { return checkout; }
    public void setCheckout(String checkout) { this.checkout = checkout; }

    public int getEstrelas() { return estrelas; }
    public void setEstrelas(int estrelas) { this.estrelas = estrelas; }

    public double getPrecoNoite() { return precoNoite; }
    public void setPrecoNoite(double precoNoite) { this.precoNoite = precoNoite; }
}
