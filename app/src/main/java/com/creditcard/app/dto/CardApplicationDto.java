package com.creditcard.app.dto;

import com.creditcard.app.model.CardType;
import jakarta.validation.constraints.*;

public class CardApplicationDto {

    @NotBlank(message = "Customer name is required")
    @Size(min = 3, max = 100, message = "Name must be between 3 and 100 characters")
    private String customerName;

    @NotBlank(message = "Email address is required")
    @Email(message = "Please enter a valid email address")
    private String email;

    @NotNull(message = "Please select a card type")
    private CardType cardType;

    @NotNull(message = "Requested credit limit is required")
    @Min(value = 10000, message = "Minimum credit limit requested must be at least ₹10,000")
    @Max(value = 1000000, message = "Maximum credit limit cannot exceed ₹10,00,000")
    private Double creditLimit;

    @NotNull(message = "Annual income is required")
    @Min(value = 100000, message = "Annual income must be greater than ₹1,00,000")
    private Double annualIncome;

    @NotBlank(message = "Please select employment status")
    private String employmentStatus;

    public CardApplicationDto() {}

    public String getCustomerName() {
        return customerName;
    }

    public void setCustomerName(String customerName) {
        this.customerName = customerName;
    }

    public String getEmail() {
        return email;
    }

    public void setEmail(String email) {
        this.email = email;
    }

    public CardType getCardType() {
        return cardType;
    }

    public void setCardType(CardType cardType) {
        this.cardType = cardType;
    }

    public Double getCreditLimit() {
        return creditLimit;
    }

    public void setCreditLimit(Double creditLimit) {
        this.creditLimit = creditLimit;
    }

    public Double getAnnualIncome() {
        return annualIncome;
    }

    public void setAnnualIncome(Double annualIncome) {
        this.annualIncome = annualIncome;
    }

    public String getEmploymentStatus() {
        return employmentStatus;
    }

    public void setEmploymentStatus(String employmentStatus) {
        this.employmentStatus = employmentStatus;
    }
}
