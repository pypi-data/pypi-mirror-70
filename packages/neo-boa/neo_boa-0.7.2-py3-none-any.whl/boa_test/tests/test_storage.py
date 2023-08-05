from boa_test.tests.boa_test import BoaFixtureTest
from neo.Settings import settings
from boa.compiler import Compiler
from neo.Prompt.Commands.BuildNRun import TestBuild
import os
import shutil
from logzero import logger
from neo.Blockchain import GetBlockchain

settings.USE_DEBUG_STORAGE = True
settings.DEBUG_STORAGE_PATH = './fixtures/debugstorage'


class TestContract(BoaFixtureTest):

    @classmethod
    def tearDownClass(cls):
        super(BoaFixtureTest, cls).tearDownClass()
        try:
            if os.path.exists(settings.debug_storage_leveldb_path):

                shutil.rmtree(settings.debug_storage_leveldb_path)
            else:
                logger.error("debug storage path doesn't exist")
        except Exception as e:
            logger.error("couldn't remove debug storage %s " % e)

    def test_Storage(self):
        output = Compiler.instance().load('%s/boa_test/example/blockchain/StorageTest.py' % TestContract.dirname).default
        out = output.write()

        snapshot = GetBlockchain()._db.createSnapshot()

        tx, results, total_ops, engine = TestBuild(out, ['sget', 'something', 'blah'], self.GetWallet1(), '070505', '05', snapshot=snapshot)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetByteArray(), b'')

        tx, results, total_ops, engine = TestBuild(out, ['sput', 'something', 'blah'], self.GetWallet1(), '070505', '05', snapshot=snapshot)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetByteArray(), b'\x01')

        tx, results, total_ops, engine = TestBuild(out, ['sget', 'something', 'blah'], self.GetWallet1(), '070505', '05', snapshot=snapshot)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetByteArray(), b'blah')

        tx, results, total_ops, engine = TestBuild(out, ['sdel', 'something', 'blah'], self.GetWallet1(), '070505', '05', snapshot=snapshot)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetByteArray(), b'\x01')

        tx, results, total_ops, engine = TestBuild(out, ['sget', 'something', 'blah'], self.GetWallet1(), '070505', '05', snapshot=snapshot)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetByteArray(), b'')

    def test_Storage2(self):
        output = Compiler.instance().load('%s/boa_test/example/blockchain/StorageTest.py' % TestContract.dirname).default
        out = output.write()

        snapshot = GetBlockchain()._db.createSnapshot()

        tx, results, total_ops, engine = TestBuild(out, ['sget', 100, 10000000000], self.GetWallet1(), '070505', '05', snapshot=snapshot)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetByteArray(), b'')

        tx, results, total_ops, engine = TestBuild(out, ['sput', 100, 10000000000], self.GetWallet1(), '070505', '05', snapshot=snapshot)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetByteArray(), b'\x01')

        tx, results, total_ops, engine = TestBuild(out, ['sget', 100, 10000000000], self.GetWallet1(), '070505', '05', snapshot=snapshot)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetBigInteger(), 10000000000)

        tx, results, total_ops, engine = TestBuild(out, ['sdel', 100, 10000000000], self.GetWallet1(), '070505', '05', snapshot=snapshot)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetByteArray(), b'\x01')

        tx, results, total_ops, engine = TestBuild(out, ['sget', 100, 10000000000], self.GetWallet1(), '070505', '05', snapshot=snapshot)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetByteArray(), b'')
