import unittest

from runtime.mediahub_runtime.state_authority import *

AUTH=AuthorizationContext("operator",True,frozenset({"state.write"}))
RESTORE_AUTH=AuthorizationContext("operator",True,frozenset({"state.restore"}))

def cmd(i,op="set",path=("devices","lamp"),value=True,gen=None,auth=AUTH):
    return Command(i,"corr-"+i,op,path,value,gen,auth)

class StateAuthorityTests(unittest.TestCase):
    def test_valid_mutation_and_event(self):
        sa=StateAuthority(); seen=[]; sa.subscribe(seen.append)
        e=sa.execute(cmd("c1"))
        self.assertEqual(sa.read()["devices"]["lamp"],True); self.assertEqual(e.command_id,"c1")
        self.assertEqual(e.correlation_id,"corr-c1"); self.assertEqual(seen,[e]); self.assertEqual(e.generation,1)
    def test_unauthenticated_and_unauthorized_are_denied(self):
        with self.assertRaises(AuthorizationDenied): StateAuthority().execute(cmd("c2",auth=None))
        bad=AuthorizationContext("user",True,frozenset())
        with self.assertRaises(AuthorizationDenied): StateAuthority().execute(cmd("c3",auth=bad))
    def test_stale_writer_is_rejected_atomically(self):
        sa=StateAuthority(); sa.execute(cmd("c4")); before=sa.read()
        with self.assertRaises(ConflictDetected): sa.execute(cmd("c5",gen=0))
        self.assertEqual(sa.read(),before); self.assertEqual(sa.metadata()["generation"],1)
    def test_duplicate_command_is_rejected(self):
        sa=StateAuthority(); first=sa.execute(cmd("c6"))
        with self.assertRaises(DuplicateCommand): sa.execute(cmd("c6",value=False))
        self.assertEqual(sa.read()["devices"]["lamp"],True); self.assertEqual(sa.events(),(first,))
    def test_invalid_input_has_no_mutation(self):
        sa=StateAuthority()
        with self.assertRaises(InvalidCommand): sa.execute(cmd("c7",path=()))
        self.assertEqual(sa.read(),{}); self.assertEqual(sa.metadata()["generation"],0)
    def test_unavailable_authority_fails_closed(self):
        sa=StateAuthority(); sa.set_available(False)
        with self.assertRaises(AuthorityUnavailable): sa.execute(cmd("c8"))
        with self.assertRaises(AuthorityUnavailable): sa.read()
    def test_checkpoint_token_and_restore(self):
        sa=StateAuthority(); sa.execute(cmd("c9")); checkpoint=sa.checkpoint(); sa.execute(cmd("c10",path=("x",),value=1))
        sa.restore(checkpoint, RESTORE_AUTH); self.assertEqual(sa.read()["devices"]["lamp"],True); self.assertNotIn("x",sa.read())
        forged=("wrong",{},0,0,0,(),())
        with self.assertRaises(AuthorizationDenied): sa.restore(forged, RESTORE_AUTH)
    def test_read_returns_copy_not_authority(self):
        sa=StateAuthority({"x":{"y":1}}); view=sa.read(); view["x"]["y"]=99
        self.assertEqual(sa.read()["x"]["y"],1)
    def test_delete_is_governed(self):
        sa=StateAuthority({"x":1}); sa.execute(cmd("c11","delete",("x",)))
        self.assertEqual(sa.read(),{})

if __name__=="__main__": unittest.main()
