#!/usr/bin/env python3
"""
Fix database consistency issues identified by validation script.
"""

import os
import sys
import sqlite3
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def fix_okr_updates_consistency():
    """Fix inconsistency between key_results.current_value and the latest update value."""
    try:
        # Connect to the database
        db_path = "organization.db"
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Find inconsistencies
        cursor.execute("""
            SELECT kr.key_result_id, kr.current_value, 
                (SELECT new_value 
                FROM okr_updates 
                WHERE key_result_id = kr.key_result_id 
                ORDER BY update_date DESC 
                LIMIT 1) as latest_update_value
            FROM key_results kr
            WHERE kr.current_value != (
                SELECT new_value
                FROM okr_updates
                WHERE key_result_id = kr.key_result_id
                ORDER BY update_date DESC
                LIMIT 1
            )
        """)
        
        # Log inconsistencies
        inconsistencies = cursor.fetchall()
        logger.info(f'Found {len(inconsistencies)} inconsistencies:')
        for kr_id, current_val, latest_val in inconsistencies:
            logger.info(f'Key Result {kr_id}: current_value={current_val}, latest_update={latest_val}')
        
        # Update the key results to match the latest update value
        cursor.execute("""
            UPDATE key_results
            SET current_value = (
                SELECT new_value 
                FROM okr_updates 
                WHERE key_result_id = key_results.key_result_id 
                ORDER BY update_date DESC 
                LIMIT 1
            )
            WHERE key_result_id IN (
                SELECT kr.key_result_id
                FROM key_results kr
                WHERE kr.current_value != (
                    SELECT new_value
                    FROM okr_updates
                    WHERE key_result_id = kr.key_result_id
                    ORDER BY update_date DESC
                    LIMIT 1
                )
            )
        """)
        
        # Commit the changes
        conn.commit()
        logger.info(f'Updated {cursor.rowcount} key results to match their latest update values')
        
        # Close connection
        conn.close()
        return True
    except sqlite3.Error as e:
        logger.error(f"Database error: {e}")
        return False
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return False

if __name__ == "__main__":
    logger.info("Starting database consistency fixes...")
    
    # Fix OKR updates consistency
    if fix_okr_updates_consistency():
        logger.info("OKR updates consistency fix completed successfully!")
    else:
        logger.error("Failed to fix OKR updates consistency.")