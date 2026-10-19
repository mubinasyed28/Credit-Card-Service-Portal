package com.creditcard.app.repository;

import com.creditcard.app.model.CardStatus;
import com.creditcard.app.model.CreditCard;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;

@Repository
public interface CreditCardRepository extends JpaRepository<CreditCard, Long> {

    Optional<CreditCard> findByCardNumber(String cardNumber);

    Optional<CreditCard> findByEmail(String email);

    long countByStatus(CardStatus status);

    @Query("SELECT c FROM CreditCard c WHERE " +
           "(:query IS NULL OR LOWER(c.customerName) LIKE LOWER(CONCAT('%', :query, '%')) OR LOWER(c.cardNumber) LIKE LOWER(CONCAT('%', :query, '%'))) " +
           "AND (:status IS NULL OR c.status = :status)")
    List<CreditCard> searchCards(@Param("query") String query, @Param("status") CardStatus status);
}
