<!-- The MainView of the configuration page
    which has a topic selection in the sidebar and the actual config page in main content -->

<template>
    <ContentLayout>
        <template v-slot:sidebar>
            <div id="nav-config">
             <h2> Konfiguration </h2>

                <li>
                    <ul>
                        <router-link tag="a" class="pageLink" to="/konfiguration/zutaten">
                            Zutatenliste
                        </router-link>
                    </ul>

                    <ul>
                        <router-link tag="a" class="pageLink" to="/konfiguration/profil">
                            Mein Profil
                        </router-link>
                    </ul>
                </li>
            </div>
        </template>

        <template v-slot:content>
            <router-view />
        </template>

        <template v-slot:actions>
            <b-button> <b-icon-info-circle /> </b-button>
        </template>
    </ContentLayout>
</template>

<script>
import ContentLayout from 'components/layout/ContentLayout.vue'

export default {
    name: 'configuration',
    components: {
        ContentLayout
    }
}
</script>

<style scoped>
    #nav-config a {
        color: #f4eeea;
        text-shadow: 0 1px 1px #32251B;
        font-size: 1.2em;
    }

    #nav-config a.active {
        color: yellow;
    }

    #nav-config li {
        list-style: none;
        margin: 0 1em 0 1em;
    }
</style>