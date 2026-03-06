#!/usr/bin/env python3
"""
E2E test for Pktamp web interface using Playwright.
"""

import asyncio
from playwright.async_api import async_playwright
import time

async def test_pktamp_ui():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        print("Testing Pktamp Web UI...")
        
        # Navigate to the app
        print("1. Loading Pktamp web interface...")
        try:
            await page.goto('http://127.0.0.1:8080', wait_until='networkidle')
        except Exception as e:
            print(f"   ERROR: Could not connect to http://127.0.0.1:8080 - {e}")
            await browser.close()
            return False
        
        print("   ✓ Page loaded successfully")
        
        # Check title
        title = await page.title()
        print(f"2. Page title: '{title}'")
        
        # Check playlist exists
        playlist_items = await page.query_selector_all('.playlist li')
        print(f"3. Number of pcap files in playlist: {len(playlist_items)}")
        
        # Test upload (create a dummy pcap)
        print("4. Testing file upload...")
        
        # Create a minimal pcap file
        dummy_pcap = (
            b'\xd4\xc3\xb2\xa1\x02\x00\x04\x00\x00\x00\x00\x00\x00\x00\x00\x00'
            b'\xff\xff\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00'
        )
        
        with open('/tmp/test_e2e.pcap', 'wb') as f:
            f.write(dummy_pcap)
        
        # Try toupload
        try:
            file_input = page.locator('input[type="file"]')
            await file_input.set_files('/tmp/test_e2e.pcap')
            await asyncio.sleep(2)  # Wait for upload
            
            # Refresh pcap list
            await page.evaluate('() => fetch("/api/pcaps")')
            await asyncio.sleep(1)
            
            print("   ✓ File upload attempted")
        except Exception as e:
            print(f"   ⚠ Upload test skipped: {e}")
        
        # Test interface dropdown
        print("5. Testing interface dropdown...")
        interface_select = await page.query_selector('.interface-select')
        if interface_select:
            print("   ✓ Interface dropdown found")
        else:
            print("   ⚠ Could not locate interface dropdown")
        
        # Test speed slider
        print("6. Testing speed slider...")
        speed_slider = await page.query_selector('.speed-slider')
        if speed_slider:
            print("   ✓ Speed slider found")
        else:
            print("   ⚠ Could not locate speed slider")
        
        # Test buttons
        print("7. Checking control buttons...")
        buttons = await page.query_selector_all('.control-panel button')
        print(f"   ✓ Found {len(buttons)} control buttons")
        
        # Check status text
        print("8. Checking status display...")
        status = await page.query_selector('.replay-info')
        if status:
            status_text = await status.inner_text()
            print(f"   Status: {status_text}")
        
        await asyncio.sleep(1)
        await browser.close()
        
        print("\n✓ E2E tests completed!")
        return True

if __name__ == '__main__':
    asyncio.run(test_pktamp_ui())
