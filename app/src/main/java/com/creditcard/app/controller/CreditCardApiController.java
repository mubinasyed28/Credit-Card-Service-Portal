package com.creditcard.app.controller;

import com.creditcard.app.dto.CardApplicationDto;
import com.creditcard.app.model.CardStatus;
import com.creditcard.app.model.CreditCard;
import com.creditcard.app.service.CreditCardService;
import jakarta.validation.Valid;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/api")
public class CreditCardApiController {

    private final CreditCardService service;

    @Autowired
    public CreditCardApiController(CreditCardService service) {
        this.service = service;
    }

    @GetMapping("/cards")
    public ResponseEntity<List<CreditCard>> getAllCards(
            @RequestParam(value = "query", required = false) String query,
            @RequestParam(value = "status", required = false) CardStatus status) {
        List<CreditCard> cards = service.searchCards(query, status);
        return ResponseEntity.ok(cards);
    }

    @GetMapping("/cards/{id}")
    public ResponseEntity<CreditCard> getCardById(@PathVariable("id") Long id) {
        return service.getCardById(id)
                .map(ResponseEntity::ok)
                .orElse(ResponseEntity.notFound().build());
    }

    @PostMapping("/cards")
    public ResponseEntity<CreditCard> applyForCard(@Valid @RequestBody CardApplicationDto dto) {
        CreditCard saved = service.applyForCard(dto);
        return ResponseEntity.status(HttpStatus.CREATED).body(saved);
    }

    @PutMapping("/cards/{id}/limit")
    public ResponseEntity<CreditCard> updateCreditLimit(
            @PathVariable("id") Long id,
            @RequestParam("newLimit") Double newLimit) {
        try {
            CreditCard updated = service.updateCreditLimit(id, newLimit);
            return ResponseEntity.ok(updated);
        } catch (IllegalArgumentException ex) {
            return ResponseEntity.badRequest().build();
        }
    }

    @PutMapping("/cards/{id}/status")
    public ResponseEntity<CreditCard> updateStatus(
            @PathVariable("id") Long id,
            @RequestParam("status") CardStatus status) {
        CreditCard updated;
        switch (status) {
            case ACTIVE:
                updated = service.approveCard(id);
                break;
            case BLOCKED:
                updated = service.blockCard(id);
                break;
            case REJECTED:
                updated = service.rejectCard(id);
                break;
            default:
                return ResponseEntity.badRequest().build();
        }
        return ResponseEntity.ok(updated);
    }

    @GetMapping("/metrics")
    public ResponseEntity<Map<String, Long>> getMetrics() {
        return ResponseEntity.ok(service.getMetrics());
    }

    @GetMapping(value = "/health", produces = org.springframework.http.MediaType.APPLICATION_JSON_VALUE)
    public ResponseEntity<Map<String, Object>> getHealth() {
        return ResponseEntity.ok(Map.of(
            "status", "UP",
            "application", "Credit Card Service Portal",
            "components", Map.of(
                "db", Map.of("status", "UP", "database", "H2 In-Memory"),
                "ping", Map.of("status", "UP")
            ),
            "timestamp", java.time.Instant.now().toString()
        ));
    }
}
