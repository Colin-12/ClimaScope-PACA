# Raw File Notes — ClimaScope-PACA

## DRIAS pilot export
- Format: CSV
- Separator: `;`
- Metadata lines start with `#`
- Columns:
  - `date`
  - `latitude`
  - `longitude`
  - `tasAdjust`
  - `prtotAdjust`

## Unit conversions
- `tasAdjust` is in Kelvin
  - target unit: Celsius
  - formula: `tas_c = tasAdjust - 273.15`

- `prtotAdjust` is in kg/m²/s
  - target unit: mm/day
  - formula: `pr_mm_day = prtotAdjust * 86400`

## Notes
- One row = one day for one grid point
- Projection period validated: 2031-01-01 to 2060-12-31
- Scenario validated: RCP4.5
