package com.creditcard.app.controller;

import com.creditcard.app.dto.CardApplicationDto;
import com.creditcard.app.model.CardStatus;
import com.creditcard.app.model.CardType;
import com.creditcard.app.model.CreditCard;
import com.creditcard.app.service.CreditCardService;
import jakarta.validation.Valid;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.validation.BindingResult;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.servlet.mvc.support.RedirectAttributes;

import java.util.List;
import java.util.Map;

@Controller
public class CreditCardController {

    private final CreditCardService service;

    @Autowired
    public CreditCardController(CreditCardService service) {
        this.service = service;
    }

    @GetMapping("/")
    public String dashboard(Model model) {
        Map<String, Long> metrics = service.getMetrics();
        model.addAttribute("metrics", metrics);
        List<CreditCard> recentCards = service.getAllCards();
        model.addAttribute("recentCards", recentCards.size() > 5 ? recentCards.subList(recentCards.size() - 5, recentCards.size()) : recentCards);
        return "dashboard";
    }

    @GetMapping("/cards")
    public String cardDirectory(@RequestParam(value = "query", required = false) String query,
                                @RequestParam(value = "status", required = false) CardStatus status,
                                Model model) {
        List<CreditCard> cards = service.searchCards(query, status);
        model.addAttribute("cards", cards);
        model.addAttribute("query", query != null ? query : "");
        model.addAttribute("selectedStatus", status);
        model.addAttribute("allStatuses", CardStatus.values());
        model.addAttribute("metrics", service.getMetrics());
        return "cards";
    }

    @GetMapping("/apply")
    public String showApplicationForm(Model model) {
        if (!model.containsAttribute("applicationDto")) {
            model.addAttribute("applicationDto", new CardApplicationDto());
        }
        model.addAttribute("cardTypes", CardType.values());
        return "apply";
    }

    @PostMapping("/apply")
    public String submitApplication(@Valid @ModelAttribute("applicationDto") CardApplicationDto dto,
                                    BindingResult bindingResult,
                                    Model model,
                                    RedirectAttributes redirectAttributes) {
        if (bindingResult.hasErrors()) {
            model.addAttribute("cardTypes", CardType.values());
            return "apply";
        }

        Double maxEligible = service.calculateMaxEligibleLimit(dto.getAnnualIncome(), dto.getCardType());
        CreditCard savedCard = service.applyForCard(dto);
        String msg = "Application submitted successfully! Application ID: #" + savedCard.getId() + " (" + savedCard.getCardNumber() + ")";
        if (dto.getCreditLimit() > maxEligible) {
            msg += " (Note: Credit limit capped at eligibility ceiling of INR " + String.format("%.0f", maxEligible) + ")";
        }
        redirectAttributes.addFlashAttribute("successMessage", msg);
        return "redirect:/cards";
    }

    @PostMapping("/cards/{id}/approve")
    public String approveCard(@PathVariable("id") Long id, RedirectAttributes redirectAttributes) {
        CreditCard card = service.approveCard(id);
        redirectAttributes.addFlashAttribute("successMessage", "Card #" + id + " has been APPROVED and ACTIVATED.");
        return "redirect:/cards";
    }

    @PostMapping("/cards/{id}/block")
    public String blockCard(@PathVariable("id") Long id, RedirectAttributes redirectAttributes) {
        CreditCard card = service.blockCard(id);
        redirectAttributes.addFlashAttribute("warningMessage", "Card #" + id + " has been FROZEN (BLOCKED).");
        return "redirect:/cards";
    }

    @PostMapping("/cards/{id}/unblock")
    public String unblockCard(@PathVariable("id") Long id, RedirectAttributes redirectAttributes) {
        CreditCard card = service.unblockCard(id);
        redirectAttributes.addFlashAttribute("successMessage", "Card #" + id + " has been RESTORED to ACTIVE status.");
        return "redirect:/cards";
    }

    @PostMapping("/cards/{id}/reject")
    public String rejectCard(@PathVariable("id") Long id, RedirectAttributes redirectAttributes) {
        CreditCard card = service.rejectCard(id);
        redirectAttributes.addFlashAttribute("errorMessage", "Application #" + id + " has been REJECTED.");
        return "redirect:/cards";
    }
}
