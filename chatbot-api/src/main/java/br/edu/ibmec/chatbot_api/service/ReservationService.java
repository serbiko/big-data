package br.edu.ibmec.chatbot_api.service;

import br.edu.ibmec.chatbot_api.models.Reservation;
import br.edu.ibmec.chatbot_api.models.ReservationStatus;
import br.edu.ibmec.chatbot_api.models.ReservationType;
import org.springframework.stereotype.Service;

import java.util.Collections;
import java.util.HashMap;
import java.util.Map;

@Service
public class ReservationService {
    private final Map<String, Reservation> store = Collections.synchronizedMap(new HashMap<>());

    public ReservationService() {
        // exemplos iniciais
        store.put("RES123", new Reservation(
                "RES123",
                ReservationType.VOO,
                ReservationStatus.CONFIRMADA,
                "Voo LATAM Rio → São Paulo em 2025-10-10, 08:30"
        ));
        store.put("HOT456", new Reservation(
                "HOT456",
                ReservationType.HOTEL,
                ReservationStatus.PENDENTE,
                "Hotel Centro (Rio), 2025-10-12 a 2025-10-15"
        ));
    }

    public Reservation get(String id) {
        return store.get(id);
    }

    public Reservation cancel(String id) {
        Reservation r = store.get(id);
        if (r != null) {
            r.setStatus(ReservationStatus.CANCELADA);
        }
        return r;
    }
}
