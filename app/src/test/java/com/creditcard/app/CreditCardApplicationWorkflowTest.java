package com.creditcard.app;

import com.creditcard.app.dto.CardApplicationDto;
import com.creditcard.app.model.CardStatus;
import com.creditcard.app.model.CardType;
import com.creditcard.app.model.CreditCard;
import com.creditcard.app.service.CreditCardService;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;

import static org.junit.jupiter.api.Assertions.*;

@SpringBootTest
public class CreditCardApplicationWorkflowTest {

    @Autowired
    private CreditCardService service;

    @Test
    @DisplayName("Feature 1 - Test 1: Calculate Max Eligible Limit Based on 40% Income")
    public void testMaxEligibleLimitCalculation() {
        // Annual income: 10,00,000 -> 40% = 4,00,000
        // Platinum max limit is 5,00,000, so eligible limit should be 4,00,000
        Double eligible = service.calculateMaxEligibleLimit(1000000.0, CardType.PLATINUM);
        assertEquals(400000.0, eligible, "Eligible limit should be 40% of annual income");

        // Titanium max limit is 1,00,000. With 10,00,000 income, 40% is 4,00,000 but capped at 1,00,000
        Double titaniumEligible = service.calculateMaxEligibleLimit(1000000.0, CardType.TITANIUM);
        assertEquals(100000.0, titaniumEligible, "Limit should be capped at Card Tier maximum ceiling");
    }

    @Test
    @DisplayName("Feature 1 - Test 2: Verify Eligibility Gate for Requested Limit")
    public void testIsEligibleForRequestedLimit() {
        // Income: 5,00,000 -> 40% = 2,00,000
        boolean valid = service.isEligibleForRequestedLimit(500000.0, CardType.GOLD, 150000.0);
        assertTrue(valid, "1,50,000 is within 2,00,000 eligibility ceiling");

        boolean invalid = service.isEligibleForRequestedLimit(500000.0, CardType.GOLD, 250000.0);
        assertFalse(invalid, "2,50,000 exceeds 2,00,000 income eligibility ceiling");
    }

    @Test
    @DisplayName("Feature 1 - Test 3: Application Creation Automatically Caps Exceeded Limit")
    public void testApplicationLimitCapping() {
        CardApplicationDto dto = new CardApplicationDto();
        dto.setCustomerName("Devika Menon");
        dto.setEmail("devika.menon@example.com");
        dto.setCardType(CardType.GOLD); // max 2,50,000
        dto.setAnnualIncome(400000.0);  // 40% = 1,60,000
        dto.setCreditLimit(220000.0);   // Requests 2,20,000 which exceeds 1,60,000
        dto.setEmploymentStatus("Salaried");

        CreditCard card = service.applyForCard(dto);
        assertNotNull(card.getId());
        assertEquals(CardStatus.PENDING, card.getStatus());
        assertEquals(160000.0, card.getCreditLimit(), "Approved limit should be automatically capped at 1,60,000");
    }
}
