package br.edu.ibmec.chatbot_api.controller;

import br.edu.ibmec.chatbot_api.models.Reservation;
import br.edu.ibmec.chatbot_api.service.ReservationService;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/reservations")
@CrossOrigin
public class ReservationController {

    private final ReservationService service;

    public ReservationController(ReservationService service) {
        this.service = service;
    }

    @GetMapping("/{id}")
    public ResponseEntity<Reservation> get(@PathVariable String id) {
        Reservation r = service.get(id);
        if (r == null) return ResponseEntity.notFound().build();
        return ResponseEntity.ok(r);
    }

    @GetMapping("/{id}/status")
    public ResponseEntity<String> status(@PathVariable String id) {
        Reservation r = service.get(id);
        if (r == null) return ResponseEntity.notFound().build();
        return ResponseEntity.ok(r.getStatus().name());
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<Void> cancel(@PathVariable String id) {
        Reservation r = service.cancel(id);
        if (r == null) return ResponseEntity.notFound().build();
        return ResponseEntity.ok().build();
    }
}
