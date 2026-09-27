# Bob Custom Rules for COLLAPSE

1. **Observer Mode**: In Observer mode, you may read files, search the codebase, and run tests. You are strictly FORBIDDEN from editing or modifying code until `prove` succeeds.
2. **Anti-Cheat Enforcement**:
   - Never add `time.sleep()`.
   - Never add retry decorators or loops.
   - Never add `@pytest.mark.skip` or `@pytest.mark.xfail`.
   - Never delete tests or weaken assertions.
3. **Verification**: Never claim a test is "fixed" without running `verify` (30 runs including trigger condition).
