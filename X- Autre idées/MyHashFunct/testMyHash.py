import hashlib, MyHash, random, unittest, time, numpy

random

alpha = "".join([chr(random.randint(0, 150)) for i in range(30)])
print(alpha)
class TestSha(unittest.TestCase):
    def test_sha1(self):
        alpha = 'abcdefghijklmnopqrstuvwxyz'

        for l in range(129):
            data = ""
            for i in range(5 * l):
                data += random.choice(alpha)

            self.assertEqual(hashlib.sha1(data.encode()).hexdigest(), MyHash.sha1(data))

        print("Pas d'erreur sur la fonction sha1")

    def test_sha256(self):
        alpha = 'abcdefghijklmnopqrstuvwxyz'

        for l in range(129):
            data = ""
            for i in range(5 * l):
                data += random.choice(alpha)

            self.assertEqual(hashlib.sha256(data.encode()).hexdigest(), MyHash.sha256(data))

        print("Pas d'erreur sur la fonction sha256")

    def test_md5(self):
        alpha = 'abcdefghijklmnopqrstuvwxyz'

        for l in range(129):
            data = ""
            for i in range(5 * l):
                data += random.choice(alpha)

            self.assertEqual(hashlib.md5(data.encode()).hexdigest(), MyHash.MD5(data))

        print("Pas d'erreur sur la fonction md5")

    def duree_sha1(self, boucle = 200):
        alpha = 'abcdefghijklmnopqrstuvwxyz'

        start_time = time.time()
        for l in range(boucle):
            data = ""
            for i in range(5 * l):
                data += random.choice(alpha)

            a = hashlib.sha1(data.encode()).hexdigest()

        print("Temps d'execution de la fonction python sha1 : {}".format(str(time.time() - start_time)))

        timer = []
        start_time = time.time()
        for l in range(boucle):
            data = ""
            for i in range(5 * l):
                data += random.choice(alpha)

            a = MyHash.sha1(data)
        print("Temps d'execution de ma fonction sha1 : {}".format(str(time.time() - start_time)))

    def duree_sha256(self, boucle = 200):
        alpha = 'abcdefghijklmnopqrstuvwxyz'

        start_time = time.time()
        for l in range(boucle):
            data = ""
            for i in range(5 * l):
                data += random.choice(alpha)

            a = hashlib.sha256(data.encode()).hexdigest()
        print("Temps d'execution de la fonction python sha256 : {}".format(str(time.time() - start_time)))

        start_time = time.time()
        for l in range(boucle):
            data = ""
            for i in range(5 * l):
                data += random.choice(alpha)

            a = MyHash.sha256(data)
        print("Temps d'execution de ma fonction sha256 : {}".format(str(time.time() - start_time)))


TestSha().test_sha1()
TestSha().test_sha256()
TestSha().test_md5()
TestSha().duree_sha1(100)
TestSha().duree_sha256(100)