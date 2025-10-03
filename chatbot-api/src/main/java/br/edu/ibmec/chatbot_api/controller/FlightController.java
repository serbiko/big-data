package br.edu.ibmec.chatbot_api.controller;

import br.edu.ibmec.chatbot_api.dto.FlightOption;
import br.edu.ibmec.chatbot_api.dto.FlightSearchRequest;
import org.springframework.web.bind.annotation.*;

import java.util.Arrays;
import java.util.List;

@RestController
@RequestMapping("/api/flights")
@CrossOrigin
public class FlightController {

    @PostMapping("/search")
    public List<FlightOption> search(@RequestBody FlightSearchRequest req) {
        return Arrays.asList(
            new FlightOption("LATAM", req.getOrigem(), req.getDestino(), req.getData(), "08:30", 599.90),
            new FlightOption("GOL",   req.getOrigem(), req.getDestino(), req.getData(), "14:10", 549.00),
            new FlightOption("Azul",  req.getOrigem(), req.getDestino(), req.getData(), "19:45", 629.50)
        );
    }
}

