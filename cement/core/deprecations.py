"""Cement core deprecation tracking and warning emission."""

from warnings import warn

#: Mapping of deprecation IDs to their human-readable warning messages.
#: The ID format is ``<since-version>-<sequence>`` (e.g. ``3.0.10-1``).
#: ``deprecate()`` looks up the message by ID and appends a GitBook URL
#: that points downstream readers at the canonical migration narrative.
DEPRECATIONS = {
    '3.0.8-1': "Environment variable CEMENT_FRAMEWORK_LOGGING is deprecated in favor of CEMENT_LOG, and will be removed in Cement v3.2.0",  # noqa: E501
    '3.0.8-2': "App.Meta.framework_logging will be changed or removed in Cement v3.2.0",  # noqa: E501
    '3.0.10-1': "The FATAL logging facility is deprecated in favor of CRITICAL, and will be removed in Cement v3.2.0",  # noqa: E501
    '3.0.16-1': "SMTPMailHandler.send() returning bool is deprecated. It will return the smtplib senderrs dict in Cement v3.2.0",  # noqa: E501
}


def deprecate(deprecation_id: str) -> None:
    """Emit a ``DeprecationWarning`` for the given deprecation ID.

    Looks up the message in :data:`DEPRECATIONS` and appends a
    ``See: https://docs.builtoncement.com/release-information/deprecations#<id>``
    fragment so users can jump from the runtime warning to the GitBook
    migration narrative.

    Args:
        deprecation_id (str): The deprecation ID to emit (e.g. ``3.0.10-1``).
            Must be a key in :data:`DEPRECATIONS`.

    """
    deprecation_id = str(deprecation_id)
    msg = DEPRECATIONS[deprecation_id]
    total_msg = f"{msg}. See: https://docs.builtoncement.com/release-information/deprecations#{deprecation_id}"  # noqa: E501
    warn(total_msg, DeprecationWarning, stacklevel=2)
