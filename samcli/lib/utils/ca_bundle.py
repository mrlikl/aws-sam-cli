"""
Utility to read ca_bundle from AWS credentials/config file
"""

import os
from typing import Optional

from botocore.session import Session


def get_ca_bundle_from_profile(profile: Optional[str] = None) -> Optional[str]:
    """
    Get ca_bundle configuration from AWS credentials or config file for the given profile.
    
    Parameters
    ----------
    profile : Optional[str]
        AWS profile name. If None, uses default profile.
    
    Returns
    -------
    Optional[str]
        Path to the ca_bundle file if configured, None otherwise.
    """
    try:
        session = Session(profile=profile)
        # get_config_variable checks both config file and environment variables
        # Priority: env var > config file
        ca_bundle = session.get_config_variable('ca_bundle')
        
        # Expand paths like ~/path/to/cert
        if ca_bundle:
            ca_bundle = os.path.expanduser(ca_bundle)
            # Verify the file exists
            if os.path.isfile(ca_bundle):
                return ca_bundle
        
        return None
    except Exception:
        return None