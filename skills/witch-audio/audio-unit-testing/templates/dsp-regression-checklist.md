# DSP Regression Checklist

Target module:
Build/version:

## Deterministic checks
- [ ] no NaN / inf
- [ ] stable reset behavior
- [ ] expected output range
- [ ] silence behavior
- [ ] extreme parameter behavior

## Comparison checks
- [ ] null test against prior build if applicable
- [ ] frequency response check if applicable
- [ ] golden file comparison if applicable

## Human checks
- [ ] quick listening pass
- [ ] harshness / click / instability scan
- [ ] automation sanity if applicable

## Notes
Biggest risk:
Best next test:
