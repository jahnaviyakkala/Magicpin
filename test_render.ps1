$BASE = "https://magicpin-jltl.onrender.com"
$VERSION = [int](Get-Date -UFormat %s)
$TRIGGER_ID = "trg_$VERSION"

Write-Host "=== 1. Health Check ===" -ForegroundColor Cyan
Invoke-RestMethod -Uri "$BASE/v1/healthz" | ConvertTo-Json

Write-Host "`n=== 2. Adding Merchant ===" -ForegroundColor Cyan
$merchantBody = @{
    scope = "merchant"
    context_id = "m_001"
    version = $VERSION
    payload = @{
        name = "Test Restaurant"
        category = "restaurant"
        rating = 3.2
        listing_score = 40
        response_rate = 0.3
        last_active_days = 5
        offers = 0
    }
} | ConvertTo-Json -Depth 5
Invoke-RestMethod -Uri "$BASE/v1/context" -Method Post -ContentType "application/json" -Body $merchantBody | ConvertTo-Json

Write-Host "`n=== 3. Adding Trigger ===" -ForegroundColor Cyan
$triggerBody = @{
    scope = "trigger"
    context_id = $TRIGGER_ID
    version = $VERSION
    payload = @{
        type = "festival"
        value = "Diwali"
    }
} | ConvertTo-Json -Depth 5
Invoke-RestMethod -Uri "$BASE/v1/context" -Method Post -ContentType "application/json" -Body $triggerBody | ConvertTo-Json

Write-Host "`n=== 4. Tick (AI Action Output) ===" -ForegroundColor Green
$tickBody = @{
    now = "2026-05-02T10:00:00Z"
    available_triggers = @($TRIGGER_ID)
} | ConvertTo-Json
$result = Invoke-RestMethod -Uri "$BASE/v1/tick" -Method Post -ContentType "application/json" -Body $tickBody

Write-Host "`nMerchant ID : $($result.actions[0].merchant_id)"
Write-Host "Trigger ID  : $($result.actions[0].trigger_id)"
Write-Host "Body        : $($result.actions[0].body)"
Write-Host "CTA         : $($result.actions[0].cta)"
Write-Host "Suppression : $($result.actions[0].suppression_key)"
