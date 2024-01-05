# Examples

`clocking` opens up a world of possibilities for tracking your time over the various working days;
you can also use it to track your work and the time spent on it across various projects.
Below, you will find many real examples.

## Tracking my working time

Suppose you work for a company as an employee, so you want to track the days you worked on various projects.
Let's start creating a profile that reflects us.

```console
clocking config --daily-hours 8 \       # Max standard hours per day
                --extraordinary 1 \     # Min extraordinary hours per day
                --permit-hours 1 \      # Min permit hours per day
                --other-hours 1 \       # Min other hours per day
                --working-days Mon Tue Wed Thu Fri \     # Working days
                --disease "I have fever" \       # Standard text for disease
                --holiday "Wow! I'm in pause" \  # Standard text for holiday
                --currency "€" \        # Select currency
                --hour-reward 8 \       # Reward for one hour
                --extraordinary-reward 10 \ # Reward for one extraordinary hour
                --food-ticket 7 \       # Reward for one food ticket
                --location "Milan Office" \ # Standard location
                --other-reward 7 \       # Reward for one other hour
                --empty-value "Im not worked today" # Standard empty value for no entry
```