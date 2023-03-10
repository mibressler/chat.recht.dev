import * as React from "react";
import { DefaultButton, TextField, Image, Text, Stack, Spinner, List, mergeStyleSets, getFocusStyle, getTheme, Icon } from "@fluentui/react";
import Progress from "./Progress";
import { useLazyGetReferencesQuery, useLazyGetRulingQuery } from "./api";
import { useState } from "react";

/* global Word, require */

// Tokens definition
const verticalGapStackTokens = {
  childrenGap: 20,
  padding: 20,
};

export default function App({title, isOfficeInitialized}) {

  const [ prompt, setPrompt ] = useState("");
  const [ showRuling, setShowRuling ] = useState(false);
  const [ trigger, { data, isFetching } ] = useLazyGetReferencesQuery();
  const [ triggerGetRuling, { data: rulingData, isFetching: rulingIsFetching }] = useLazyGetRulingQuery();
  const theme = getTheme();
  const { palette, semanticColors, fonts } = theme;

  const click = () => {
      if (prompt != undefined) {
        setShowRuling(false);
        trigger(prompt);
      }
  };

  if (!isOfficeInitialized) {
    return (
      <Progress
        title={title}
        logo={require("./../../../assets/logo-filled.png")}
        message="Loading, please wait..."
      />
    );
  }


  function convertData(data) {
    const res = [];
    data.forEach(element => {
      res.push({
        'name': element['id'],
        'score': element['score'],
        'summary': element['summary'],
        'court_name': element['metadata']['court']['name'],
        'date': element['metadata']['date']
      })
    });
    return res;
  }

  const classNames = mergeStyleSets({
    itemCell: [
      getFocusStyle(theme, { inset: -1 }),
      {
        minHeight: 54,
        padding: 10,
        boxSizing: 'border-box',
        borderBottom: `1px solid ${semanticColors.bodyDivider}`,
        display: 'flex',
        cursor: 'pointer',
        selectors: {
          '&:hover': { background: palette.neutralLight },
        },
      },
    ],
    itemImage: {
      flexShrink: 0,
    },
    itemContent: {
      marginLeft: 10,
      overflow: 'hidden',
      flexGrow: 1,
    },
    itemName: [
      fonts.xLarge,
      {
        whiteSpace: 'nowrap',
        overflow: 'hidden',
        textOverflow: 'ellipsis',
      },
    ],
    itemIndex: {
      fontSize: fonts.small.fontSize,
      color: palette.neutralTertiary,
      marginBottom: 10,
    },
    chevron: {
      alignSelf: 'center',
      marginLeft: 10,
      color: palette.neutralTertiary,
      fontSize: fonts.large.fontSize,
      flexShrink: 0,
    },
    itemSummary: {
      '-webkit-mask-image': "-webkit-gradient(linear, 100% 50%, 100% 98%, from(rgba(0,0,0,1)), to(rgba(0,0,0,0)))",
    }
  });

  const onRenderCell = (item, _) => {
    return (
      <div className={classNames.itemCell} data-is-focusable={true} onClick={() => {
        triggerGetRuling(item.name);
        setShowRuling(true);
      }}>
        <div className={classNames.itemContent}>
          <div className={classNames.itemName}>{item.court_name} vom {formatDate(item.date)}</div>
          <div className={classNames.itemIndex}>Score {item.score}</div>
          <div className={classNames.itemSummary}>{item.summary}</div>
        </div>
        <Icon className={classNames.chevron} iconName={'ChevronRight'} />
      </div>
    );
  };

  function formatDate(input) {
    let dateStr = "";
    let date = new Date(Date.parse(input));
    if (date == NaN) {
      dateStr = input;
    } else {
      const options = { year: 'numeric', month: '2-digit', day: '2-digit' };
      dateStr = date.toLocaleDateString('de-DE', options);
    }
    return dateStr;
  }

  function renderList() {
    if(showRuling) {
      return (
        <Stack>
          <Stack.Item>
            <Stack horizontal>
              <Stack.Item grow={1}>
                <DefaultButton className="ms-welcome__action" iconProps={{ iconName: "ChevronLeft" }} onClick={() => {
                    setShowRuling(false);
                  }}>
                  Zur??ck
                </DefaultButton>
              </Stack.Item>
              <Stack.Item hidden={rulingIsFetching} >
                <DefaultButton className="ms-welcome__action" iconProps={{ iconName: "TextDocument" }} onClick={() => {
                    Word.run(async (context) => {
                      let textToInsert = `(${rulingData.metadata.court.name}, ${rulingData.metadata.type} vom ${formatDate(rulingData.metadata.date)} ??? ${rulingData.metadata.file_number})`;
                      let selection = context.document.getSelection();
                      selection.load();
                      await context.sync();
                      if (selection.isEmpty) {
                        // Add text after the cursor
                        selection.insertText(textToInsert, Word.InsertLocation.after);
                      } else {
                        // Replace selected text
                        selection.insertText(textToInsert, Word.InsertLocation.replace);
                      }
                      await context.sync();
                    });
                  }}>
                  Zitat f??r dieses Urteil einf??gen
                </DefaultButton>
              </Stack.Item>
            </Stack>
          </Stack.Item>
          <Stack.Item>
          { rulingIsFetching ? <Spinner /> : <div dangerouslySetInnerHTML={{ "__html": rulingData.content}}></div> }
          </Stack.Item>
        </Stack>
      )
    } else {
      return (
        <List items={convertData(data['data'])} onRenderCell={onRenderCell} />
      )
    }
  }

  return (
    <Stack horizontal horizontalAlign='space-between' grow>
      <Stack.Item grow>
        <Stack tokens={verticalGapStackTokens}>
          <Stack.Item align="start">
            <Text variant={'large'}>
              <b>Nach Urteilen Suchen</b>
            </Text>
          </Stack.Item>
          <Stack.Item align="stretch">
            <TextField placeholder='Suchbegriff(e)' value={prompt} onChange={(_, newValue) => {
              setPrompt(newValue);
            }}/>
          </Stack.Item>
          <Stack.Item align="center">
            <DefaultButton className="ms-welcome__action" iconProps={{ iconName: "ChevronRight" }} onClick={click}>
              Suchen
            </DefaultButton>
          </Stack.Item>
          <Stack.Item align="center">
            {
              isFetching && <Spinner />
            }
          </Stack.Item>
          <Stack.Item align="stretch">
            { !isFetching && data && renderList() }
          </Stack.Item>
        </Stack>
      </Stack.Item>
      <Stack.Item>
        <Image width={100} src={require("./../../../assets/icon-128.png")} />
      </Stack.Item>
    </Stack>
  );
}
