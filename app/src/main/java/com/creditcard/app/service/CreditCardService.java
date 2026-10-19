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

    public Double calculateMaxEligibleLimit(Double annualIncome, CardType cardType) {
        if (annualIncome == null || annualIncome <= 0) {
            return 0.0;
        }
        double incomeCap = annualIncome * 0.40;
        return Math.min(incomeCap, cardType.getMaxLimit());
    }

    public boolean isEligibleForRequestedLimit(Double annualIncome, CardType cardType, Double requestedLimit) {
        if (requestedLimit == null || requestedLimit <= 0) {
            return false;
        }
        Double maxEligible = calculateMaxEligibleLimit(annualIncome, cardType);
        return requestedLimit <= maxEligible;
    }

    public CreditCard applyForCard(CardApplicationDto dto) {
        Double maxEligible = calculateMaxEligibleLimit(dto.getAnnualIncome(), dto.getCardType());
        Double finalLimit = Math.min(dto.getCreditLimit(), maxEligible);
        String generatedCardNumber = generateMaskedCardNumber();
        CreditCard card = new CreditCard(
                generatedCardNumber,
                dto.getCustomerName().trim(),
                dto.getEmail().trim(),
                dto.getCardType(),
                finalLimit,
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
        long total = repository.count();
        long active = repository.countByStatus(CardStatus.ACTIVE);
        metrics.put("total", total);
        metrics.put("active", active);
        metrics.put("pending", repository.countByStatus(CardStatus.PENDING));
        metrics.put("blocked", repository.countByStatus(CardStatus.BLOCKED));
        metrics.put("rejected", repository.countByStatus(CardStatus.REJECTED));
        long approvalRate = total > 0 ? (active * 100 / total) : 0L;
        metrics.put("approvalRate", approvalRate);
        return metrics;
    }

    private String generateMaskedCardNumber() {
        int last4 = 1000 + random.nextInt(9000);
        return "****-****-****-" + last4;
    }
}
