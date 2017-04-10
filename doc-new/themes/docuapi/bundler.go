// Copyright 2016 Bjørn Erik Pedersen <bjorn.erik.pedersen@gmail.com>s. All rights reserved.
//
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
// http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

package main

import (
	"bufio"
	"bytes"
	"flag"
	"fmt"
	"io"
	"io/ioutil"
	"log"
	"os"
	"os/exec"
	"path/filepath"
	"strings"

	"github.com/tdewolff/minify"
	"github.com/tdewolff/minify/js"

	shutil "github.com/termie/go-shutil"
	libsass "github.com/wellington/go-libsass"
)

const (

	// The source for the styles and scripts.
	// If you have Slate locally, set the slate flag.
	slateRepo = "https://github.com/lord/slate.git"
)

var (
	logger *log.Logger = log.New(os.Stdout, "bundler: ", log.Ldate|log.Ltime|log.Lshortfile)

	staticSlateDirs = []string{
		"images",
		"fonts",
	}
)

func main() {

	var (
		slateSourceDir = flag.String("slate", "", "the path to the Slate source, if not set it will be cloned from "+slateRepo)
		minify         = flag.Bool("minify", true, "apply minification to output Javascript, CSS etc.")
	)

	flag.Parse()

	pwd, err := os.Getwd()

	if err != nil {
		logger.Fatal(err)
	}

	bundler := newBundler(
		*slateSourceDir,
		filepath.Join(pwd, "static", "slate"), *minify)

	if err := bundler.init(); err != nil {
		logger.Fatal(err)
	}

	if err := bundler.fetchSlateIfNeeded(); err != nil {
		logger.Fatal(err)
	}

	if err := bundler.replaceSlateSourcesInTheme(); err != nil {
		logger.Fatal("Failed to move Slate sources: ", err)
	}

	if err := bundler.mergeAndAdjustStyles(); err != nil {
		logger.Fatal("Failed to edit Slate sources: ", err)
	}

	if err := bundler.createJSBundles(); err != nil {
		logger.Fatal("Failed to bundle JS: ", err)
	}

	if err := bundler.compileSassSources(); err != nil {
		logger.Fatal("Failed compile SASS stylesheets: ", err)
	}

	logger.Println("Done...")

}

type bundler struct {
	slateSource string
	slateTarget string

	minify bool

	// We do some mods to the Slate source (add some styles). Do that on a copy in here.
	tmpSlateSource string

	logger *log.Logger
}

func newBundler(slateSource, slateTarget string, minify bool) *bundler {
	return &bundler{slateSource: slateSource, slateTarget: slateTarget, minify: minify, logger: logger}
}

func (b *bundler) init() error {
	if err := os.RemoveAll(b.slateTarget); err != nil {
		return err
	}

	if err := os.MkdirAll(b.slateTarget, os.ModePerm); err != nil {
		return err
	}

	return nil
}

func (b *bundler) fetchSlateIfNeeded() error {
	if b.slateSource != "" {
		b.logger.Println("Use existing Slate clone in", b.slateSource)
		if err := b.copySlateSourcesToModify(); err != nil {
			return err
		}
		return nil
	}

	b.logger.Println("Fetch Slate from", slateRepo)

	slateSource, err := ioutil.TempDir("", "docuapi")

	if err != nil {
		return fmt.Errorf("Failed to create tmpdir: %s", err)
	}

	if err := cloneSlateInto(slateSource); err != nil {
		return fmt.Errorf("Failed to clone Slate: %s", err)
	}

	b.slateSource = slateSource

	// This will be replaced on next build, so it is tempoary enough.
	b.tmpSlateSource = slateSource

	return nil
}

func (b *bundler) copySlateSourcesToModify() error {
	slateSource, err := ioutil.TempDir("", "docuapi")

	if err != nil {
		return fmt.Errorf("Failed to create tmpdir: %s", err)
	}

	// We need to adapt the SASS source ... or learn how to use includeDirs ...
	if err := shutil.CopyTree(
		filepath.Join(b.slateSource, "source", "stylesheets"),
		filepath.Join(slateSource, "source", "stylesheets"), nil); err != nil {
		return fmt.Errorf("Failed to copy stylesheets: %s", err)
	}

	b.tmpSlateSource = slateSource

	return nil
}

func (b *bundler) replaceSlateSourcesInTheme() error {
	for _, staticDir := range staticSlateDirs {
		b.logger.Println("Copy", staticDir)
		if err := shutil.CopyTree(filepath.Join(b.slateSource, "source", staticDir), filepath.Join(b.slateTarget, staticDir), nil); err != nil {
			return err
		}
	}
	return nil
}

func (b *bundler) mergeAndAdjustStyles() error {
	slateStylesheetsDir := filepath.Join(b.tmpSlateSource, "source", "stylesheets")
	b.logger.Println("Compile SASS in", slateStylesheetsDir)

	customImports := filepath.Join(b.slateTarget, "..", "..", "assets", "stylesheets")

	// Copy custom SASS files into merged source. Should be able to do this by
	// setting an includePath, but ...
	fis, err := ioutil.ReadDir(customImports)

	if err != nil {
		return err
	}

	for _, fi := range fis {
		if err := shutil.CopyFile(filepath.Join(customImports, fi.Name()), filepath.Join(slateStylesheetsDir, fi.Name()), false); err != nil {
			return fmt.Errorf("failed to copy custom SASS: %s", err)
		}
	}

	// Insert custom import
	if err := replaceInFile(filepath.Join(slateStylesheetsDir, "screen.css.scss"),
		"@import 'variables';\n@import 'icon-font';",
		"@import 'variables';\n@import 'icon-font';\n@import 'docuapi';"); err != nil {
		return err
	}

	return nil
}

func replaceInFile(filename, old, new string) error {
	read, err := ioutil.ReadFile(filename)
	if err != nil {
		return err
	}
	nc := bytes.Replace(read, []byte(old), []byte(new), -1)

	err = ioutil.WriteFile(filename, nc, os.ModePerm)
	if err != nil {
		return err
	}
	return nil
}

func (b *bundler) compileSassSources() error {
	source := filepath.Join(b.tmpSlateSource, "source", "stylesheets")
	target := filepath.Join(b.slateTarget, "stylesheets")
	os.MkdirAll(target, os.ModePerm)

	fis, err := ioutil.ReadDir(source)
	if err != nil {
		return err
	}

	for _, fi := range fis {
		if strings.HasPrefix(fi.Name(), "_") {
			continue
		}

		targetName := strings.TrimSuffix(fi.Name(), ".scss")

		b.logger.Println("Compile", fi.Name(), "to", targetName)

		cssFile, err := os.Create(filepath.Join(target, targetName))
		if err != nil {
			return err
		}

		outputStyle := libsass.NESTED_STYLE

		if b.minify {
			outputStyle = libsass.COMPRESSED_STYLE
		}

		comp, err := libsass.New(cssFile, nil,
			libsass.OutputStyle(outputStyle),
			libsass.Path(filepath.Join(source, fi.Name())),
		)

		if err != nil {
			return err
		}

		if err := comp.Run(); err != nil {
			return fmt.Errorf("SASS run failed: %s", err)
		}

	}

	return nil
}

func (b *bundler) createJSBundles() error {
	src := filepath.Join(b.slateSource, "source", "javascripts")
	dst := filepath.Join(b.slateTarget, "javascripts")
	overrides := filepath.Join(b.slateTarget, "..", "..", "assets", "javascripts")
	jsB := newJSBundler(src, dst, overrides, b.minify)
	return jsB.bundle()
}

func cloneSlateInto(dir string) error {
	logger.Println("Clone Slate into", dir, "...")

	cmd := exec.Command("git", "clone", "-b", "docuapi", slateRepo, dir)
	return cmd.Run()
}

type jsBundler struct {
	src string
	dst string

	minify bool

	overridesSrc string
	overrides    map[string][]byte

	logger *log.Logger

	// Per bundle
	seen map[string]bool
	buff bytes.Buffer
}

func newJSBundler(src, dst, overridesSrc string, minify bool) *jsBundler {
	return &jsBundler{src: src, dst: dst, overridesSrc: overridesSrc, minify: minify, logger: logger, overrides: make(map[string][]byte)}
}

func (j *jsBundler) readOverrides() error {
	j.logger.Println("Looking for overrides in", j.overridesSrc)
	return filepath.Walk(j.overridesSrc, func(path string, info os.FileInfo, err error) error {
		if info.IsDir() {
			return nil
		}
		libPath := strings.TrimPrefix(path, j.overridesSrc)
		libPath = strings.TrimPrefix(libPath, string(filepath.Separator))
		j.logger.Println("Adding override:", libPath)

		libContent, err := ioutil.ReadFile(path)
		if err != nil {
			return err
		}

		j.overrides[libPath] = libContent

		return nil
	})

}

func (j *jsBundler) bundle() error {

	if err := j.readOverrides(); err != nil {
		return err
	}

	if err := os.MkdirAll(j.dst, os.ModePerm); err != nil {
		return err
	}

	fis, err := ioutil.ReadDir(j.src)
	if err != nil {
		return err
	}

	for _, fi := range fis {
		if !strings.HasSuffix(fi.Name(), ".js") {
			continue
		}

		filename := filepath.Join(j.src, fi.Name())
		if err := j.newBundle(filename); err != nil {
			return err
		}

		var source bytes.Buffer

		if j.minify {
			j.logger.Println("Minify JS")
			m := minify.New()
			m.AddFunc("text/javascript", js.Minify)
			if err := m.Minify("text/javascript", &source, &j.buff); err != nil {
				return err
			}
		} else {
			source = j.buff
		}

		if err = ioutil.WriteFile(filepath.Join(j.dst, fi.Name()), source.Bytes(), os.ModePerm); err != nil {
			return fmt.Errorf("Failed to write to destination: %s", err)
		}

	}

	return nil
}

func (j *jsBundler) newBundle(filename string) error {
	j.logger.Println("New bundle from ", filename)
	j.seen = make(map[string]bool)
	j.buff.Reset()

	j.buff.WriteString("\n\n// From bep's Poor Man's JS bundler // ----\n")

	return j.handleFile(filename)
}

func (j *jsBundler) handleFile(filename string) error {

	var (
		overridenContent = j.getOverrideIfFound(filename)
		currDir          = filepath.Dir(filename)
		libs             []string
	)

	if overridenContent == nil {
		file, err := os.Open(filename)
		if err != nil {
			return err
		}

		// TODO(bep) exclude the requires when writing to bundle
		libs = j.extractRequiredLibs(file)

		file.Close()
	} else {
		libs = j.extractRequiredLibs(bytes.NewReader(overridenContent))
	}

	for _, lib := range libs {
		if j.seen[lib] {
			continue
		}

		j.seen[lib] = true

		lib += ".js"
		libFilename := filepath.Join(currDir, lib)

		//j.logger.Println("Handle lib", lib)

		// Must write its dependencies first
		if err := j.handleFile(libFilename); err != nil {
			return err
		}

		var content []byte
		var err error

		content = j.getOverrideIfFound(libFilename)

		if content == nil {
			content, err = ioutil.ReadFile(libFilename)
			if err != nil {
				return err
			}
		}

		_, err = j.buff.Write(content)
		if err != nil {
			return err
		}

	}

	return nil
}

func (j *jsBundler) getOverrideIfFound(filename string) []byte {
	libPath := strings.TrimPrefix(filename, j.src)
	libPath = strings.TrimPrefix(libPath, string(filepath.Separator))
	return j.overrides[libPath]
}

func (j *jsBundler) extractRequiredLibs(r io.Reader) []string {
	const require = "//= require"
	scanner := bufio.NewScanner(r)
	var libs []string
	for scanner.Scan() {
		t := strings.TrimSpace(scanner.Text())
		if strings.HasPrefix(t, require) {
			libs = append(libs, strings.TrimSpace(t[len(require):]))
		}
	}
	return libs
}
