$merchantBody = @"
{
  "scope": "merchant",
  "context_id": "m_001",
  "version": 1,
  "payload": {
    "name": "Test Restaurant",
    "category": "restaurant",
    "rating": 3.2,
    "listing_score": 40,
    "response_rate": 0.3,
    "last_active_days": 5
  }
}
"@

$triggerBody = @"
{
  "scope": "trigger",
  "context_id": "trg_001",
  "version": 1,
  "payload": {
    "type": "festival"
  }
}
"@

$tickBody = @"
{
  "now": "2026-04-29T10:30:00Z",
  "available_triggers": ["trg_001"]
}
"@

Write-Host "Adding merchant..."
Invoke-RestMethod -Uri "http://127.0.0.1:8000/v1/context" -Method Post -ContentType "application/json" -Body $merchantBody

Write-Host "Adding trigger..."
Invoke-RestMethod -Uri "http://127.0.0.1:8000/v1/context" -Method Post -ContentType "application/json" -Body $triggerBody

Write-Host "Calling /tick..."
$response = Invoke-RestMethod -Uri "http://127.0.0.1:8000/v1/tick" -Method Post -ContentType "application/json" -Body $tickBody

Write-Host "TICK RESPONSE:"
$response | ConvertTo-Json -Depth 5
