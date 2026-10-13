# Quality check triage

Initial frozen head: `39c528d6a221b3520fbbd7a33f7650e7e49b5e43`;
base: `2cd4d9bd947fbd1aff25c6bec28e98f3fc1b1c13`;
full-index patch SHA256: `172e496f52b9a96e421813261ae98f13f1c96aec89412b9ff4869ff6ed94ecb1`.

Independent quality checker ran the complete suite once: exit 1, 277 tests,
625.998 seconds, 22 failing assertions/subtests. Every failure was in the existing
ValidationTests positive source fixtures and reported
`Quality framework: Required filesystem path is absent`.

Independent read-only triage `quality_check_triage` confirmed QCHECK-1 before
repair: setUp copied schemas/examples but omitted the now-required central
standards catalog. Production source and trusted-base validators already passed.
The command-as-data failure at tests/test_validation.py:422 therefore reported
missing fixture data rather than candidate command execution.

Decision: **confirmed**, P2, fixture completeness. Add the actual standards
directory to the setUp copy list. Preserve every assertion, including marker
absence and command nonexecution; do not weaken the production guard. The consumer
fixture keeps its original migration behavior. No additional test methods are
needed for this fixture alignment.

The failed run remains recorded. Focused and complete corrected checks are required
before formal Full review. This is development check triage, not implementation
approval or independent Full review.

Repair implemented: one fixture copy-list addition, no production change or
assertion change. `python -m unittest tests.test_validation -v` exited 0:
50 tests in 60.126 seconds, OK. The complete corrected run is still required.
