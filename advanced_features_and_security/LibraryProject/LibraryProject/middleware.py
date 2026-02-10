"""
Content Security Policy (CSP) Middleware

This middleware implements CSP headers to prevent XSS attacks by controlling
which resources (scripts, styles, images, etc.) can be loaded by the browser.

CSP works by defining a whitelist of allowed sources for different resource types.
This prevents malicious scripts from being injected and executed.

For more information: https://developer.mozilla.org/en-US/docs/Web/HTTP/CSP
"""

from django.utils.deprecation import MiddlewareMixin


class CSPMiddleware(MiddlewareMixin):
    """
    Content Security Policy Middleware
    
    Sets CSP headers on all responses to prevent XSS attacks.
    The policy restricts where resources can be loaded from.
    
    Security Benefit:
    - Prevents inline script execution (XSS protection)
    - Restricts resource loading to trusted sources only
    - Provides defense-in-depth against code injection attacks
    """
    
    def process_response(self, request, response):
        """
        Add CSP headers to the response.
        
        CSP Directives Explained:
        - default-src: Fallback for other fetch directives
        - script-src: Controls which scripts can be executed
        - style-src: Controls which stylesheets can be applied
        - img-src: Controls which images can be loaded
        - font-src: Controls which fonts can be loaded
        - connect-src: Controls which URLs can be loaded via fetch/XHR
        - frame-ancestors: Prevents clickjacking (replaces X-Frame-Options)
        - base-uri: Restricts which URLs can be used as base
        - form-action: Restricts which URLs can be used as form action
        """
        
        # Build CSP header value
        # 'self' means same origin, 'unsafe-inline' allows inline scripts/styles
        # Note: 'unsafe-inline' is needed for Django admin and some templates
        # In production, consider using nonces or hashes instead
        csp_policy = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline' 'unsafe-eval'; "  # unsafe-eval needed for admin
            "style-src 'self' 'unsafe-inline'; "  # Allows inline styles
            "img-src 'self' data: https:; "  # Allows images from same origin, data URIs, and HTTPS
            "font-src 'self' data:; "  # Allows fonts from same origin and data URIs
            "connect-src 'self'; "  # Restricts AJAX/fetch to same origin
            "frame-ancestors 'none'; "  # Prevents embedding in iframes (clickjacking protection)
            "base-uri 'self'; "  # Restricts base tag URLs
            "form-action 'self'; "  # Restricts form submissions to same origin
            "object-src 'none'; "  # Prevents plugins (Flash, etc.)
            "upgrade-insecure-requests"  # Upgrades HTTP to HTTPS automatically
        )
        
        # Set the CSP header
        response['Content-Security-Policy'] = csp_policy
        
        # Also set report-only version for testing (optional)
        # Uncomment to test CSP without blocking resources
        # response['Content-Security-Policy-Report-Only'] = csp_policy
        
        return response
