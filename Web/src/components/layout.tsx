import Head from "next/head";
import Image from "next/image";
import styles from "./layout.module.css";
import utilStyles from "../styles/utils.module.css";
import Link from "next/link";

interface LayoutProps {
  children: React.ReactNode;
  title: string;
}

function getTitle(title: string): string {
  let resTitle = "InnoID";
  if (title) {
    resTitle += `- ${title}`;
  }
  return resTitle;
}

export default function Layout({ children, title }: LayoutProps): JSX.Element {
  return (
    <div className={styles.container}>
      <Head>
        <link rel="icon" href="/icons8-favicon-50.png" />
        <title>{getTitle(title)}</title>
      </Head>
      <header className={styles.header}>some header</header>
      <main>{children}</main>
    </div>
  );
}
