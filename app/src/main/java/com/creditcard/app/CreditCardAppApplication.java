package com.creditcard.app;

import com.creditcard.app.model.CardStatus;
import com.creditcard.app.model.CardType;
import com.creditcard.app.model.CreditCard;
import com.creditcard.app.repository.CreditCardRepository;
import org.springframework.boot.CommandLineRunner;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.Bean;

@SpringBootApplication
public class CreditCardAppApplication {

    public static void main(String[] args) {
        SpringApplication.run(CreditCardAppApplication.class, args);
    }

    @Bean
    public CommandLineRunner initDatabase(CreditCardRepository repository) {
        return args -> {
            if (repository.count() == 0) {
                repository.save(new CreditCard("****-****-****-4821", "Aarav Sharma", "aarav.sharma@example.com",
                        CardType.PLATINUM, 350000.0, 1200000.0, "Salaried", CardStatus.ACTIVE));
                repository.save(new CreditCard("****-****-****-9154", "Priya Patel", "priya.patel@example.com",
                        CardType.GOLD, 200000.0, 850000.0, "Self-Employed", CardStatus.PENDING));
                repository.save(new CreditCard("****-****-****-6372", "Rohan Verma", "rohan.verma@example.com",
                        CardType.TITANIUM, 80000.0, 450000.0, "Salaried", CardStatus.BLOCKED));
                repository.save(new CreditCard("****-****-****-2048", "Ananya Iyer", "ananya.iyer@example.com",
                        CardType.PLATINUM, 450000.0, 1500000.0, "Salaried", CardStatus.ACTIVE));
                System.out.println(">>> Seed Data Initialized: 4 baseline credit card records inserted.");
            }
        };
    }
}
