# New Relic Cost Diagnostics

Quick guide to diagnose and reduce New Relic costs using NerdGraph API.

## Prerequisites

- New Relic User API Key (stored in `/home/claude/.env` as `NEW_RELIC_USER_API_KEY`)
- Account ID (find it in New Relic UI URL)
- `curl` or similar HTTP client

## 1. Get Account Information

```bash
curl -X POST https://api.newrelic.com/graphql \
  -H "Content-Type: application/json" \
  -H "API-Key: YOUR_API_KEY" \
  -d '{"query":"{ actor { accounts { id name } } }"}'
```

## 2. Check Data Ingestion by Type (Last 30 Days)

```bash
curl -X POST https://api.newrelic.com/graphql \
  -H "Content-Type: application/json" \
  -H "API-Key: YOUR_API_KEY" \
  -d '{"query":"{ actor { account(id: ACCOUNT_ID) { nrql(query: \"SELECT sum(GigabytesIngested) FROM NrConsumption WHERE productLine = '"'"'DataPlatform'"'"' FACET usageMetric SINCE 30 days ago\") { results } } } }"}'
```

**Key Metrics to Watch:**
- `TracingBytes`: Distributed tracing data (usually the biggest cost driver)
- `InfraProcessBytes`: Infrastructure process monitoring
- `LoggingBytes`: Application and system logs
- `MetricsBytes`: Metrics and timeseries data
- `BrowserEventsBytes`: Browser/RUM monitoring

## 3. Find Applications with Most Transactions

```bash
curl -X POST https://api.newrelic.com/graphql \
  -H "Content-Type: application/json" \
  -H "API-Key: YOUR_API_KEY" \
  -d '{"query":"{ actor { account(id: ACCOUNT_ID) { nrql(query: \"SELECT count(*) FROM Transaction FACET appName SINCE 7 days ago LIMIT 50\") { results } } } }"}'
```

## 4. Check Daily Ingestion Trend

```bash
curl -X POST https://api.newrelic.com/graphql \
  -H "Content-Type: application/json" \
  -H "API-Key: YOUR_API_KEY" \
  -d '{"query":"{ actor { account(id: ACCOUNT_ID) { nrql(query: \"SELECT sum(GigabytesIngested) FROM NrConsumption WHERE productLine = '"'"'DataPlatform'"'"' FACET usageMetric TIMESERIES 1 day SINCE 30 days ago\") { results } } } }"}'
```

## Common Cost Reduction Strategies

### 🔴 High Impact (Disable Distributed Tracing)

**Problem**: Distributed tracing generates 40-50% of total costs in typical setups.

**Solution**: Disable on PHP agents
```ini
# In /etc/php/X.X/mods-available/newrelic.ini
newrelic.distributed_tracing_enabled = false
newrelic.span_events.max_samples_stored = 100
```

**Expected Savings**: 40-60% cost reduction

---

### 🟡 Medium Impact (Reduce Infrastructure Process Monitoring)

**Problem**: Monitoring every process on every server is expensive.

**Solution**: Disable or reduce sampling
```yaml
# In /etc/newrelic-infra.yml
enable_process_metrics: false
# OR reduce frequency
metrics_process_sample_rate: 60  # default is 20 seconds
```

**Expected Savings**: 20-30% cost reduction

---

### 🟢 Low Impact (Optimize Logging)

**Problem**: Application logs forwarded to New Relic.

**Solution**: Disable log forwarding
```ini
# In newrelic.ini
newrelic.application_logging.enabled = false
newrelic.application_logging.forwarding.enabled = false
```

Use local log management (CloudWatch, Papertrail, etc.) which is cheaper.

**Expected Savings**: 5-10% cost reduction

---

### 🟢 Low Impact (Reduce APM Coverage)

**Problem**: Monitoring too many non-critical applications.

**Solution**: Remove New Relic agent from:
- ❌ Staging/dev environments
- ❌ Low-traffic sites (<1000 req/day)
- ❌ Internal tools
- ❌ Static sites

Keep only on business-critical production apps.

**Expected Savings**: 10-30% depending on app count

---

## Quick Cost Estimation

**New Relic Pricing** (Data Plus plan):
- First 100 GB/month: Included in base subscription
- Additional data: ~$0.30-0.50 per GB (varies by contract)

**Example Calculation**:
```
800 GB/month ingestion
- 100 GB (included)
= 700 GB billable × $0.40/GB
= $280/month in data costs
+ base subscription (~$100-200/month)
= ~$380-480/month total
```

## Troubleshooting High Costs

### Symptom: TracingBytes > 300 GB/month

**Diagnosis**: Distributed tracing enabled on too many apps or too high sampling rate.

**Fix**:
1. Disable DT globally (see above)
2. Or reduce sampling: `newrelic.span_events.max_samples_stored = 100`

---

### Symptom: InfraProcessBytes > 200 GB/month

**Diagnosis**: Process monitoring on too many servers.

**Fix**:
1. Disable process metrics: `enable_process_metrics: false`
2. Or whitelist specific processes only

---

### Symptom: LoggingBytes > 100 GB/month

**Diagnosis**: Too much application logging being forwarded.

**Fix**:
1. Disable log forwarding in New Relic
2. Use cheaper log aggregation (CloudWatch, Papertrail, Logtail)
3. Reduce application log verbosity (set to ERROR/WARNING only)

---

## Useful NRQL Queries

### Top Apps by Data Ingestion
```sql
SELECT sum(GigabytesIngested)
FROM NrConsumption
WHERE usageMetric = 'TracingBytes'
FACET consumingAccountName, appName
SINCE 30 days ago
LIMIT 20
```

### Cost Trend Over Time
```sql
SELECT sum(GigabytesIngested)
FROM NrConsumption
WHERE productLine = 'DataPlatform'
TIMESERIES 1 day
SINCE 90 days ago
```

### Hosts Sending Most Data
```sql
SELECT sum(GigabytesIngested)
FROM NrConsumption
FACET hostname
SINCE 30 days ago
LIMIT 50
```

---

## Alternative APM Solutions

If New Relic remains too expensive after optimization:

| Solution | Cost | Best For |
|----------|------|----------|
| **Sentry** | $26-99/month | Error tracking only |
| **AppSignal** | $99/month flat | PHP/Laravel apps |
| **Datadog APM** | ~$15/host/month | Per-host pricing model |
| **Grafana Cloud** | $50-200/month | Metrics + logs + traces |
| **Self-hosted Grafana Stack** | Free (DIY) | DevOps teams |

---

## Cloudways-Specific Notes

**SSH Access**: Limited (no root)

**How to Apply New Relic Config Changes**:
1. Open Cloudways support ticket
2. Request modification to New Relic PHP agent config
3. They have root access and can modify `/etc/php/X.X/mods-available/newrelic.ini`
4. Wait 24-48h for data ingestion to reflect changes

**Typical Ticket Template**: See `brain/diary/YYYY/newrelic-ticket.md` for dated examples.

---

## References

- [New Relic NerdGraph API](https://api.newrelic.com/graphql)
- [New Relic Pricing Calculator](https://newrelic.com/pricing)
- [PHP Agent Configuration](https://docs.newrelic.com/docs/apm/agents/php-agent/configuration/php-agent-configuration/)
