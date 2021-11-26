job("Build and push Docker") {
    container(image = "openjdk:11") {
        shellScript {
            content = """
                    ./generateArtifacts.sh
                    cp output /mnt/space/share
                """
        }
    }

    docker {
        beforeBuildScript {
            content = "cp /mnt/space/share docker"
        }

        build {}

        push("pilgrimagesw.registry.jetbrains.space/p/mp/mydocker/myimage")
    }
}