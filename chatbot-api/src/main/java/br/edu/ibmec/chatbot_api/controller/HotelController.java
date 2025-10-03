package br.edu.ibmec.chatbot_api.controller;

import br.edu.ibmec.chatbot_api.dto.HotelOption;
import br.edu.ibmec.chatbot_api.dto.HotelSearchRequest;
import org.springframework.web.bind.annotation.*;

import java.util.Arrays;
import java.util.List;

@RestController
@RequestMapping("/api/hotels")
@CrossOrigin
public class HotelController {

    @PostMapping("/search")
    public List<HotelOption> search(@RequestBody HotelSearchRequest req) {
        return Arrays.asList(
            new HotelOption("Hotel Centro",      req.getCidade(), req.getCheckin(), req.getCheckout(), 3, 280.0),
            new HotelOption("Palace Premium",    req.getCidade(), req.getCheckin(), req.getCheckout(), 5, 950.0),
            new HotelOption("Pousada Azul",      req.getCidade(), req.getCheckin(), req.getCheckout(), 4, 420.0),
            new HotelOption("Budget Inn",        req.getCidade(), req.getCheckin(), req.getCheckout(), 2, 180.0),
            new HotelOption("Vista Mar",         req.getCidade(), req.getCheckin(), req.getCheckout(), 4, 520.0)
        );
    }
}
