
def test_CLGrader():

  g = CLGrader()

  with g.add_test() as t:
    t.NS.FILE = "file1.txt"
    t.command = "test -e {FILE}"

  with a.add_test() as t:
    t.NS.DIR = "dir1"
    t.NS.FILE = "file.txt"

    t.commands += "test -d {DIR}"
    t.commands += "test -f {DIR}/{FILE}"

  with a.add_test() as t:
    t.NS.SCRIPTNAME = "sin.gnuplot"
    t.NS.IMAGENAME = "sin.png"

    t.directory = "gnuplot"
    t.commands += "gnuplot {SCRIPTNAME}"
    t.commands += "test -f {IMAGENAME}"

    t.on_fail = "touch {IMAGENAME}"
    t.on_success = None

  with a.add_test() as t:
    t.NS.SCRIPTNAME = "cos.gnuplot"
    t.NS.IMAGENAME = "cos.png"

    t.directory = "gnuplot"
    t.commands += "gnuplot {SCRIPTNAME}"
    t.commands += "test -f {IMAGENAME}"

    with t.add_fail_callback() as f:
      f.commands += 'gnuplot $(find_file "{SCRIPTNAME}")'
      with f.add_fail_callback() as ff:
        ff.commands += '''gnuplot -e 'set term png; set ouptut "{IMAGENAME}"' $(find_file "{SCRIPTNAME}")'''


  with a.add_test() as t:
    t.commands += "test -f {IMAGENAME}"
    t.run_if = cmd("test -e {IMAGENAME}")

  g.run()


