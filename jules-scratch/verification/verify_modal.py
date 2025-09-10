import os
from playwright.sync_api import sync_playwright, expect
import re

def run_verification():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        file_path = os.path.abspath('DH-HQ_v3.3/rosters/rosters.html')
        page.goto(f'file://{file_path}')

        page.locator('#usernameInput').fill('The_Oracle')
        page.locator('#fetchRostersButton').click()

        expect(page.locator('#leagueSelect option')).to_have_count(8, timeout=20000)
        page.select_option('#leagueSelect', index=1)

        expect(page.locator('.roster-column')).to_have_count(12, timeout=20000)

        # Find and click on Christian McCaffrey
        cmc_locator = page.locator('.player-name:has-text("C. McCaffrey")')
        expect(cmc_locator.first).to_be_visible(timeout=10000)
        cmc_locator.first.click()

        modal = page.locator('#game-logs-modal')
        expect(modal).to_be_visible(timeout=10000)

        # Wait for the summary chips to be rendered
        expect(page.locator('.summary-chip')).to_have_count(3, timeout=15000)

        # Wait for the table card container to be rendered
        expect(page.locator('.table-card-container')).to_be_visible(timeout=15000)

        page.screenshot(path='jules-scratch/verification/verification.png')

        browser.close()

if __name__ == '__main__':
    run_verification()
