package com.creditcard.app.model;

public enum CardStatus {
    PENDING("Pending Approval", "warning"),
    ACTIVE("Active / Approved", "success"),
    BLOCKED("Security Frozen", "danger"),
    REJECTED("Rejected", "secondary");

    private final String label;
    private final String badgeClass;

    CardStatus(String label, String badgeClass) {
        this.label = label;
        this.badgeClass = badgeClass;
    }

    public String getLabel() {
        return label;
    }

    public String getBadgeClass() {
        return badgeClass;
    }
}
