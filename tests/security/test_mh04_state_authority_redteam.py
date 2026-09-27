import unittest

from runtime.mediahub_runtime.state_authority import *


class StateAuthorityRedTeamTests(unittest.TestCase):
    def test_missing_auth_cannot_mutate(self):
        sa=StateAuthority()
        c=Command("rt-01","rt-corr-01","set",("security","flag"),True,authorization=None)
        with self.assertRaises(AuthorizationDenied): sa.execute(c)
        self.assertEqual(sa.read(),{})
    def test_remote_context_does_not_gain_privilege(self):
        sa=StateAuthority(); ctx=AuthorizationContext("remote",True,frozenset({"read.only"}))
        c=Command("rt-02","rt-corr-02","set",("security","flag"),True,authorization=ctx)
        with self.assertRaises(AuthorizationDenied): sa.execute(c)
    def test_event_observer_cannot_replace_canonical_state(self):
        sa=StateAuthority({"x":1})
        def observer(event):
            snapshot=sa.read(); snapshot["x"]=99
        sa.subscribe(observer); sa.execute(Command("rt-03","rt-corr-03","set",("y",),2,authorization=AuthorizationContext("op",True,frozenset({"state.write"}))))
        self.assertEqual(sa.read()["x"],1)
    def test_forged_checkpoint_rejected(self):
        sa=StateAuthority({"x":1})
        with self.assertRaises(AuthorizationDenied): sa.restore(("forged",{"x":9},0,0))
        self.assertEqual(sa.read()["x"],1)
    def test_authority_unavailability_fails_closed(self):
        sa=StateAuthority(); sa.set_available(False)
        c=Command("rt-04","rt-corr-04","set",("x",),1,authorization=AuthorizationContext("op",True,frozenset({"state.write"})))
        with self.assertRaises(AuthorityUnavailable): sa.execute(c)

if __name__=="__main__": unittest.main()
