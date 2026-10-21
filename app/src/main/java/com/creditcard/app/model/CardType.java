package com.creditcard.app.model;

public enum CardType {
    PLATINUM("Platinum Card", 500000.0),
    GOLD("Gold Card", 250000.0),
    TITANIUM("Titanium Card", 100000.0);

    private final String displayName;
    private final Double maxLimit;

    CardType(String displayName, Double maxLimit) {
        this.displayName = displayName;
        this.maxLimit = maxLimit;
    }

    public String getDisplayName() {
        return displayName;
    }

    public Double getMaxLimit() {
        return maxLimit;
    }
}
