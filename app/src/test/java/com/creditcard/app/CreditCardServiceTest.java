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

import java.util.List;
import java.util.Map;

import static org.junit.jupiter.api.Assertions.*;

@SpringBootTest
public class CreditCardServiceTest {

    @Autowired
    private CreditCardService service;

    @Test
    @DisplayName("Test 1: Verify Initial Seed Data Population")
    public void testSeedDataLoaded() {
        List<CreditCard> cards = service.getAllCards();
        assertNotNull(cards, "Card list should not be null");
        assertTrue(cards.size() >= 4, "At least 4 seed cards should exist in the repository");
    }

    @Test
    @DisplayName("Test 2: Apply for New Card Application")
    public void testApplyForCard() {
        CardApplicationDto dto = new CardApplicationDto();
        dto.setCustomerName("Vikram Singhania");
        dto.setEmail("vikram.singhania@example.com");
        dto.setCardType(CardType.GOLD);
        dto.setCreditLimit(200000.0);
        dto.setAnnualIncome(900000.0);
        dto.setEmploymentStatus("Salaried");

        CreditCard created = service.applyForCard(dto);
        assertNotNull(created.getId(), "Generated Card ID should not be null");
        assertEquals(CardStatus.PENDING, created.getStatus(), "New card application must be PENDING");
        assertTrue(created.getCardNumber().startsWith("****-****-****-"), "Card number must be masked");
    }

    @Test
    @DisplayName("Test 3: Transition Status from PENDING to ACTIVE")
    public void testApproveCard() {
        CardApplicationDto dto = new CardApplicationDto();
        dto.setCustomerName("Meera Nambiar");
        dto.setEmail("meera.nambiar@example.com");
        dto.setCardType(CardType.TITANIUM);
        dto.setCreditLimit(75000.0);
        dto.setAnnualIncome(400000.0);
        dto.setEmploymentStatus("Salaried");

        CreditCard applied = service.applyForCard(dto);
        CreditCard approved = service.approveCard(applied.getId());

        assertEquals(CardStatus.ACTIVE, approved.getStatus(), "Card status should be updated to ACTIVE");
    }

    @Test
    @DisplayName("Test 4: Emergency Freeze Card to BLOCKED")
    public void testBlockCard() {
        CardApplicationDto dto = new CardApplicationDto();
        dto.setCustomerName("Kabir Mehta");
        dto.setEmail("kabir.mehta@example.com");
        dto.setCardType(CardType.PLATINUM);
        dto.setCreditLimit(300000.0);
        dto.setAnnualIncome(1100000.0);
        dto.setEmploymentStatus("Self-Employed");

        CreditCard applied = service.applyForCard(dto);
        service.approveCard(applied.getId());
        CreditCard blocked = service.blockCard(applied.getId());

        assertEquals(CardStatus.BLOCKED, blocked.getStatus(), "Card status should be BLOCKED");
    }

    @Test
    @DisplayName("Test 5: Verify KPI Dashboard Metrics Calculation")
    public void testMetricsCalculation() {
        Map<String, Long> metrics = service.getMetrics();
        assertNotNull(metrics, "Metrics map should not be null");
        assertTrue(metrics.containsKey("total"), "Metrics must contain total count");
        assertTrue(metrics.containsKey("active"), "Metrics must contain active count");
        assertTrue(metrics.containsKey("pending"), "Metrics must contain pending count");
        assertTrue(metrics.containsKey("blocked"), "Metrics must contain blocked count");
        assertTrue(metrics.get("total") >= 4, "Total cards count should be >= 4");
    }
}
