# ASTRA-DISTRIBUTED-LOCAL-DEVELOPMENT-TOPOLOGY.md

## Controller/Authority

- `mh-dev-01`
  - Primary local pool

## Primary Local Pool

- `mh-dev-02`
  - Fast pool

## Fast Pool

- `Voktors-Mac-mini.local`

---

## Failure Closed Promotion

- Promote failures within the three permanent lanes until the worker is deemed fail-closed.
- This is done using the `fail-closed` agent, which will handle the details of selecting the appropriate lane for fail-closed promotion.

---

## No Direct Main Writes

- Prevent the worker from directly writing to the main branch.
- This is done using the `read-only` agent, which will disallow any writes to the main branch once it has been committed.

---

## No Secrets or Credentials

- Ensure that no credentials or secrets are included in the agent fabric or the execution environment.
- All sensitive information must be managed external to the agent fabric and the execution environment.

---

## Exact Target-SHA Binding

- Bind the target-SHA to the exact line in the boundary file where we want to make changes.
- This is done using the `bind-target-sha` agent, which will ensure that the target-SHA is correctly linked to the boundary file.

---

## Isolated Branches

- Maintain three separate branches for each lane: `mh-dev-01`, `mh-dev-02`, and `Voktors-Mac-mini.local`.
- This is done using the `create-branch` agent, which will create the necessary branches for each lane.

---

## GitHub Evidence Transport

- Transport evidence from each lane to the main branch using the `evidence-transmission` agent.
- This is done using the `transmit-evidence` agent, which will handle the transportation of evidence from each lane to the main branch.

---

## G5 Allow Three Simultaneous Disjoint Claims

- Support the execution of three simultaneous disjoint claims on the three lanes.
- This is done using the `g5-supported` agent, which will enable the execution of three simultaneous claims on the three lanes.

---

### Clauses to Prove

1. **Primary Local Pool State**
    - Contains `mh-dev-02` and `Voktors-Mac-mini.local` as direct claims.

2. **Fast Pool State**
    - Contains `mh-dev-02` as direct claim.

3. **Controller/Authority State**
    - Contains `mh-dev-01` and `Voktors-Mac-mini.local` as direct claims.

4. **All Lane Execution (G5=3)**
    - Ensure that all lanes can execute the job concurrently.

5. **Failure Closed Promotion**
    - Prove that the worker can be successfully promoted to the fast lane and then back to the controller/authority lane, without direct main writes or secrets.

6. **No Direct Main Writes**
    - Confirm that the worker does not directly write to the main branch once it has been committed.

7. **No Secrets or Credentials**
    - Verify that no credentials or secrets are included in the agent fabric or the execution environment.

8. **Specific Lines in the Boundary File**
    - Verify that the boundary file exactly contains the following lines:
        - `mh-dev-01`: Primary local pool
        - `mh-dev-02`: Fast pool
        - `Voktors-Mac-mini.local`: Fast pool

9. **Target-SHA Binding**
    - The target-SHA is correctly linked to the line in the boundary file where we want to make changes.

10. **Isolated Branches**
    - All three lanes have their own separate branches.

11. **GitHub Evidence Transport**
    - Evidence is successfully transmitted from each lane to the main branch.

12. **G5 Support**
    - Three simultaneous claims can be executed on the three lanes.

### Concrete Evidence

- **Verification of Agent Fabric**

  ```sh
  git push origin head
  ```

- **Target-SHA Binding**

  ```sh
  git log -n 1 > path/to/boundaryfile && ./agents/bind-target-sha -f path/to/boundaryfile < SHA
  ```

- **Failed Commit to Show Change**

  ```sh
  git commit -a -m "Update boundary file for ASTRA-DISTRIBUTED-LOCAL-DEVELOPMENT-TOPOLOGY.md"
  ```

- **Run Specific Tests**

  ```sh
  ./tests/test_agent_fabric.py --lane mh-dev-01
  ./tests/test_agent_fabric.py --lane mh-dev-02
  ./tests/test_agent_fabric.py --lane Voktors-Mac-mini.local
  ```

- **Check for Secrets or Credentials**

  ```sh
  git grep -r 'credentials' . --exclude=".git"
  git grep -r 'secrets' . --exclude=".git"
  ```

- **Check for Secret Bypasses**

  ```sh
  git blame -s path/to/boundaryfile | grep 'credentials' | grep 'secrets'
  ```
  
- **Check Regressions**

  ```sh
  ./tests/test_agent_fabric.py --lane mh-dev-01
  ./tests/test_agent_fabric.py --lane mh-dev-02
  ./tests/test_agent_fabric.py --lane Voktors-Mac-mini.local
  ```

- **Check G5 Execution**

  ```sh
  ./tests/test_agent_fabric.py --lane mh-dev-01 --lane mh-dev-02 --lane Voktors-Mac-mini.local
  ```

- **Check for Failure Closed Promotion**

  ```sh
  ./agents/fail-closed --lane mh-dev-01
  ./agents/fail-closed --lane mh-dev-02
  ./agents/fail-closed --lane Voktors-Mac-mini.local
  ```

- **Check for No Direct Main Writes**

  ```sh
  git log --branch origin/main --notmh-dev-01 --not-mh-dev-02 --not-Voktors-Mac-mini.local
  ```

- **Check for No Secrets or Credentials**

  ```sh
  git grep -r 'credentials' . --exclude=".git"
  git grep -r 'secrets' . --exclude=".git"
  ```

- **Check for GitHub Evidence Transport**

  ```sh
  git branch | grep -P "mh-dev-01|mh-dev-02|Voktors-Mac-mini.local"
  git ls-remote origin --heads -q mh-dev-01 mh-dev-02 Voktors-Mac-mini.local
  ```

These steps will demonstrate that the boundary file exactly contains the required facts and meets all the acceptance criteria, proving the real three-Claude topology through fresh evidence.
