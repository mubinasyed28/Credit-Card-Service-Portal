package com.creditcard.app.service;

import com.creditcard.app.dto.CardApplicationDto;
import com.creditcard.app.model.CardStatus;
import com.creditcard.app.model.CardType;
import com.creditcard.app.model.CreditCard;
import com.creditcard.app.repository.CreditCardRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.*;

@Service
@Transactional
public class CreditCardService {

    private final CreditCardRepository repository;
    private final Random random = new Random();

    @Autowired
    public CreditCardService(CreditCardRepository repository) {
        this.repository = repository;
    }

    public List<CreditCard> getAllCards() {
        return repository.findAll();
    }

    public Optional<CreditCard> getCardById(Long id) {
        return repository.findById(id);
    }

    public List<CreditCard> searchCards(String query, CardStatus status) {
        String cleanQuery = (query != null && !query.trim().isEmpty()) ? query.trim() : null;
        return repository.searchCards(cleanQuery, status);
    }

    public CreditCard applyForCard(CardApplicationDto dto) {
        String generatedCardNumber = generateMaskedCardNumber();
        CreditCard card = new CreditCard(
                generatedCardNumber,
                dto.getCustomerName().trim(),
                dto.getEmail().trim(),
                dto.getCardType(),
                dto.getCreditLimit(),
                dto.getAnnualIncome(),
                dto.getEmploymentStatus(),
                CardStatus.PENDING
        );
        return repository.save(card);
    }

    public CreditCard approveCard(Long id) {
        CreditCard card = repository.findById(id)
                .orElseThrow(() -> new IllegalArgumentException("Invalid Card ID: " + id));
        card.setStatus(CardStatus.ACTIVE);
        return repository.save(card);
    }

    public CreditCard blockCard(Long id) {
        CreditCard card = repository.findById(id)
                .orElseThrow(() -> new IllegalArgumentException("Invalid Card ID: " + id));
        card.setStatus(CardStatus.BLOCKED);
        return repository.save(card);
    }

    public CreditCard unblockCard(Long id) {
        CreditCard card = repository.findById(id)
                .orElseThrow(() -> new IllegalArgumentException("Invalid Card ID: " + id));
        card.setStatus(CardStatus.ACTIVE);
        return repository.save(card);
    }

    public CreditCard rejectCard(Long id) {
        CreditCard card = repository.findById(id)
                .orElseThrow(() -> new IllegalArgumentException("Invalid Card ID: " + id));
        card.setStatus(CardStatus.REJECTED);
        return repository.save(card);
    }

    public Map<String, Long> getMetrics() {
        Map<String, Long> metrics = new HashMap<>();
        metrics.put("total", repository.count());
        metrics.put("active", repository.countByStatus(CardStatus.ACTIVE));
        metrics.put("pending", repository.countByStatus(CardStatus.PENDING));
        metrics.put("blocked", repository.countByStatus(CardStatus.BLOCKED));
        return metrics;
    }

    private String generateMaskedCardNumber() {
        int last4 = 1000 + random.nextInt(9000);
        return "****-****-****-" + last4;
    }
}
