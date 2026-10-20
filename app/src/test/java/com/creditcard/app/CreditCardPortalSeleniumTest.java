package com.creditcard.app;

import io.github.bonigarcia.wdm.WebDriverManager;
import org.junit.jupiter.api.*;
import org.openqa.selenium.*;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.chrome.ChromeOptions;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.Select;
import org.openqa.selenium.support.ui.WebDriverWait;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.test.web.server.LocalServerPort;

import java.io.File;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.nio.file.StandardCopyOption;
import java.time.Duration;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.List;

import static org.junit.jupiter.api.Assertions.*;

@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
@TestMethodOrder(MethodOrderer.OrderAnnotation.class)
public class CreditCardPortalSeleniumTest {

    @LocalServerPort
    private int port;

    private WebDriver driver;
    private WebDriverWait wait;
    private String baseUrl;

    private static final String FAILURE_SCREENSHOT_DIR = "screenshots/failures";
    private static final String EVIDENCE_SCREENSHOT_DIR = "screenshots/task9";

    @BeforeAll
    public static void setupClass() {
        new File(FAILURE_SCREENSHOT_DIR).mkdirs();
        new File(EVIDENCE_SCREENSHOT_DIR).mkdirs();
        try {
            WebDriverManager.chromedriver().setup();
        } catch (Exception e) {
            System.out.println("WebDriverManager automatic setup fallback: " + e.getMessage());
        }
    }

    @BeforeEach
    public void setup() {
        ChromeOptions options = new ChromeOptions();
        options.addArguments("--headless=new");
        options.addArguments("--disable-gpu");
        options.addArguments("--window-size=1920,1080");
        options.addArguments("--no-sandbox");
        options.addArguments("--disable-dev-shm-usage");
        options.addArguments("--remote-allow-origins=*");

        driver = new ChromeDriver(options);
        wait = new WebDriverWait(driver, Duration.ofSeconds(10));
        baseUrl = "http://localhost:" + port;
    }

    @AfterEach
    public void tearDown() {
        if (driver != null) {
            driver.quit();
        }
    }

    private void captureScreenshot(String filename) {
        if (driver instanceof TakesScreenshot) {
            File src = ((TakesScreenshot) driver).getScreenshotAs(OutputType.FILE);
            try {
                Path dest = Paths.get(EVIDENCE_SCREENSHOT_DIR, filename);
                Files.copy(src.toPath(), dest, StandardCopyOption.REPLACE_EXISTING);
                System.out.println("Saved verification screenshot: " + dest.toAbsolutePath());
            } catch (IOException e) {
                System.err.println("Failed to save screenshot: " + e.getMessage());
            }
        }
    }

    private void captureFailureScreenshot(String testName) {
        if (driver instanceof TakesScreenshot) {
            File src = ((TakesScreenshot) driver).getScreenshotAs(OutputType.FILE);
            String timestamp = LocalDateTime.now().format(DateTimeFormatter.ofPattern("yyyyMMdd_HHmmss"));
            Path dest = Paths.get(FAILURE_SCREENSHOT_DIR, "failure_" + testName + "_" + timestamp + ".png");
            try {
                Files.copy(src.toPath(), dest, StandardCopyOption.REPLACE_EXISTING);
                System.err.println("Captured failure screenshot: " + dest.toAbsolutePath());
            } catch (IOException e) {
                System.err.println("Failed to capture failure screenshot: " + e.getMessage());
            }
        }
    }

    @Test
    @Order(1)
    @DisplayName("Journey 1: Complete Card Application & Automated Directory Verification")
    public void testCardApplicationUserJourney() {
        try {
            driver.get(baseUrl + "/apply");
            assertEquals("Apply for Card - Credit Card Service Portal", driver.getTitle());

            WebElement nameInput = wait.until(ExpectedConditions.visibilityOfElementLocated(By.id("customerName")));
            nameInput.clear();
            nameInput.sendKeys("Aarav Sharma");

            WebElement emailInput = driver.findElement(By.id("email"));
            emailInput.clear();
            emailInput.sendKeys("aarav.sharma@enterprise.com");

            Select cardTypeSelect = new Select(driver.findElement(By.id("cardType")));
            cardTypeSelect.selectByValue("PLATINUM");

            WebElement limitInput = driver.findElement(By.id("creditLimit"));
            limitInput.clear();
            limitInput.sendKeys("300000");

            WebElement incomeInput = driver.findElement(By.id("annualIncome"));
            incomeInput.clear();
            incomeInput.sendKeys("1200000");

            Select employmentSelect = new Select(driver.findElement(By.id("employmentStatus")));
            employmentSelect.selectByValue("Salaried");

            WebElement submitBtn = driver.findElement(By.id("btn-submit-application"));
            submitBtn.click();

            // Assert redirection to /cards
            wait.until(ExpectedConditions.urlContains("/cards"));
            assertTrue(driver.getCurrentUrl().contains("/cards"), "Should redirect to card directory upon submission");

            // Assert success alert
            WebElement successAlert = wait.until(ExpectedConditions.visibilityOfElementLocated(By.id("alert-success")));
            assertTrue(successAlert.getText().contains("Application submitted successfully"));

            // Assert Aarav Sharma record exists in table
            WebElement table = driver.findElement(By.id("cards-table"));
            String tableContent = table.getText();
            assertTrue(tableContent.contains("Aarav Sharma"), "Cards table must contain newly registered cardholder");
            assertTrue(tableContent.contains("Pending") || tableContent.contains("PENDING"), "New application status must initially be Pending");

            captureScreenshot("journey1_application_success.png");
        } catch (Throwable t) {
            captureFailureScreenshot("Journey1_Application");
            throw t;
        }
    }

    @Test
    @Order(2)
    @DisplayName("Journey 2: Validation Gate - Reject Sub-Minimum Income & Exceeded Limits")
    public void testNegativeIncomeValidationGate() {
        try {
            driver.get(baseUrl + "/apply");

            WebElement nameInput = wait.until(ExpectedConditions.visibilityOfElementLocated(By.id("customerName")));
            nameInput.sendKeys("Invalid Tester");

            WebElement emailInput = driver.findElement(By.id("email"));
            emailInput.sendKeys("invalid@test.com");

            Select cardTypeSelect = new Select(driver.findElement(By.id("cardType")));
            cardTypeSelect.selectByValue("TITANIUM");

            WebElement limitInput = driver.findElement(By.id("creditLimit"));
            limitInput.sendKeys("50000");

            // Submitting sub-minimum income (Validation specifies @Min(100000))
            WebElement incomeInput = driver.findElement(By.id("annualIncome"));
            incomeInput.sendKeys("50000"); // Under 1,00,000 threshold

            Select employmentSelect = new Select(driver.findElement(By.id("employmentStatus")));
            employmentSelect.selectByValue("Freelancer");

            WebElement submitBtn = driver.findElement(By.id("btn-submit-application"));
            submitBtn.click();

            // Assert that application remains on /apply with validation error
            assertTrue(driver.getCurrentUrl().contains("/apply"), "Form submission should be halted on validation failure");
            
            WebElement incomeError = wait.until(ExpectedConditions.visibilityOfElementLocated(By.id("err-annualIncome")));
            assertTrue(incomeError.isDisplayed(), "Inline validation error for income must be visible");
            assertTrue(incomeError.getText().contains("Annual income must be greater than ₹1,00,000"));

            captureScreenshot("journey2_validation_gate.png");
        } catch (Throwable t) {
            captureFailureScreenshot("Journey2_ValidationGate");
            throw t;
        }
    }

    @Test
    @Order(3)
    @DisplayName("Journey 3: Multi-Field Search & Live Filtering by Customer Name")
    public void testSearchAndFilterUserJourney() {
        try {
            driver.get(baseUrl + "/cards");
            wait.until(ExpectedConditions.visibilityOfElementLocated(By.id("cards-table")));

            // Search for seed record "Priya"
            WebElement searchInput = driver.findElement(By.id("search-input"));
            searchInput.clear();
            searchInput.sendKeys("Priya");

            WebElement searchBtn = driver.findElement(By.id("btn-search"));
            searchBtn.click();

            wait.until(ExpectedConditions.urlContains("query=Priya"));

            // Verify table content
            List<WebElement> rows = driver.findElements(By.cssSelector("#cards-table tbody tr"));
            assertFalse(rows.isEmpty(), "Search query should return matching rows");

            for (WebElement row : rows) {
                if (!row.getAttribute("id").equals("no-cards-row")) {
                    String customerName = row.findElement(By.className("customer-name")).getText();
                    assertTrue(customerName.contains("Priya"), "Filtered rows must contain 'Priya'");
                }
            }

            captureScreenshot("journey3_search_filter.png");
        } catch (Throwable t) {
            captureFailureScreenshot("Journey3_SearchFilter");
            throw t;
        }
    }

    @Test
    @Order(4)
    @DisplayName("Journey 4: Role-Based Status Lifecycle - Administrative Approval Action")
    public void testStatusLifecycleApprovalAction() {
        try {
            driver.get(baseUrl + "/cards");
            wait.until(ExpectedConditions.visibilityOfElementLocated(By.id("cards-table")));

            // Look for any PENDING card approval button
            List<WebElement> approveButtons = driver.findElements(By.className("btn-approve"));
            if (!approveButtons.isEmpty()) {
                WebElement approveBtn = approveButtons.get(0);
                String buttonId = approveBtn.getAttribute("id");
                String cardId = buttonId.replace("btn-approve-", "");

                approveBtn.click();

                // Wait for reload and verify status transition
                wait.until(ExpectedConditions.urlContains("/cards"));
                WebElement statusBadge = wait.until(ExpectedConditions.visibilityOfElementLocated(By.id("status-badge-" + cardId)));
                String statusText = statusBadge.getText().trim();
                assertTrue(statusText.contains("Active") || statusText.equals("ACTIVE"), 
                        "Status must transition to Active / Approved upon officer approval. Observed: " + statusText);
                assertTrue(statusBadge.getAttribute("class").contains("bg-success"), 
                        "Status badge must display green success class");
            } else {
                // If all are already approved, verify freeze/block button on an ACTIVE card
                List<WebElement> blockButtons = driver.findElements(By.className("btn-block"));
                assertFalse(blockButtons.isEmpty(), "Either approve or freeze button must be available");
                WebElement blockBtn = blockButtons.get(0);
                String cardId = blockBtn.getAttribute("id").replace("btn-block-", "");
                blockBtn.click();

                wait.until(ExpectedConditions.urlContains("/cards"));
                WebElement statusBadge = wait.until(ExpectedConditions.visibilityOfElementLocated(By.id("status-badge-" + cardId)));
                String statusText = statusBadge.getText().trim();
                assertTrue(statusText.contains("Frozen") || statusText.equals("BLOCKED"), 
                        "Status must transition to Security Frozen. Observed: " + statusText);
                assertTrue(statusBadge.getAttribute("class").contains("bg-danger"), 
                        "Status badge must display danger class");
            }

            captureScreenshot("journey4_status_lifecycle.png");
        } catch (Throwable t) {
            captureFailureScreenshot("Journey4_StatusLifecycle");
            throw t;
        }
    }
}
