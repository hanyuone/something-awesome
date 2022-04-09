<script lang="ts">
	import FileList from "./components/FileList.svelte";
	import Header from "./components/Header.svelte";
	import type UploadedFile from "./types/UploadedFile";

	const files: UploadedFile[] = JSON.parse(filesRaw).map(
		({ name, pages, time }) => {
			return {
				name: name,
				pages: pages,
				time: new Date(time),
			};
		}
	);
</script>

<main class="m-0">
	<Header />
	<FileList {files} />
</main>

<style lang="postcss" global>
	@tailwind base;
	@tailwind components;
	@tailwind utilities;
</style>
